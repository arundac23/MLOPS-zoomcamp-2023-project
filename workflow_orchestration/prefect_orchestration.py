import datetime
from IPython.display import display


from typing import List
import pathlib
import pickle
import pandas as pd
import numpy as np
import scipy
import sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error
import mlflow
import xgboost as xgb
from prefect import flow, task

@task(retries=3, retry_delay_seconds=2)
def read_data(filename: str,categorical_features: List[str], numerical_features: List[str]) -> (pd.DataFrame,pd.Series):
    
    df = pd.read_parquet(filename)

    df = df[df.trip_seconds.notnull()]
    df = df[df.trip_start_timestamp.notnull()]
    
    df = df[(df['trip_seconds'] > 60) & (df['trip_seconds'] < 3600)]

    # Create the 'duration' column in minutes as the target variable
    df['duration'] = df['trip_seconds'] / 60

    # Preprocess categorical features
    for column in categorical_features:
        df[column].fillna(-1, inplace=True)
        df[column] = df[column].astype('str')
        df[column] = df[column].str.lower().str.replace(' ', '_')

    # Select only the relevant columns
    target = ['duration']
    selected_columns = categorical_features + numerical_features+target
    df = df[selected_columns]


    return df[categorical_features + numerical_features],df[target]


@task
def build_model(
    df_train: pd.DataFrame, y_train:pd.Series, df_val: pd.DataFrame, y_val:pd.Series
) -> tuple(
    [
        scipy.sparse._csr.csr_matrix,
        scipy.sparse._csr.csr_matrix,
        np.ndarray,
        np.ndarray,
        sklearn.feature_extraction.DictVectorizer,
    ]
):
    dv = DictVectorizer()

    train_dicts = df_train.to_dict(orient="records")
    X_train = dv.fit_transform(train_dicts)

    val_dicts = df_val.to_dict(orient="records")
    X_val = dv.transform(val_dicts)

    y_train = y_train.values
    y_val = y_val.values
    return X_train, X_val, y_train, y_val, dv

@task(log_prints=True)
def train_best_model(
    X_train: scipy.sparse._csr.csr_matrix,
    X_val: scipy.sparse._csr.csr_matrix,
    y_train: np.ndarray,
    y_val: np.ndarray,
    dv: sklearn.feature_extraction.DictVectorizer,
) -> None:
    

    with mlflow.start_run():
        train = xgb.DMatrix(X_train, label=y_train)
        valid = xgb.DMatrix(X_val, label=y_val)

        best_params = {
        'learning_rate':	0.5458691870793922,
        'max_depth':	38,
        'min_child_weight':	7.968333201830882,
        'objective':	'reg:linear',
        'reg_alpha':	0.19154033738324955,
        'reg_lambda':	0.032825863134369984,
        'seed':	42
        }

        mlflow.log_params(best_params)

        booster = xgb.train(
            params=best_params,
            dtrain=train,
            num_boost_round=200,
            evals=[(valid, "validation")],
            early_stopping_rounds=20,
        )

        y_pred = booster.predict(valid)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)

        pathlib.Path("models").mkdir(exist_ok=True)
        with open("models/preprocessor.b", "wb") as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")

        mlflow.xgboost.log_model(booster, artifact_path="models_mlflow")
    

        markdown__rmse_report = f"""# RMSE Report

## Summary

Duration Prediction 

## RMSE XGBoost Model

| Region    | RMSE |
|:----------|-------:|
| {date.today()} | {rmse:.2f} |
"""

        create_markdown_artifact(
            key="duration-model-report", markdown=markdown__rmse_report
        )

    return None

@flow
def main_flow(
    train_path: str = "./workflow_orchestration/data/chicago_taxi_train_dataset_2023-01.parquet",
    val_path: str = "./workflow_orchestration/data/chicago_taxi_Val_dataset_2023-02.parquet",
) -> None:
    """The main training pipeline"""

    # MLflow settings
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("chicago-taxi-experiment")

    # Load
    df_train,y_train = read_data(train_path,
        categorical_features=['pickup_community_area','dropoff_community_area'],
        numerical_features=[])
    df_val,y_val = read_data(val_path,
        categorical_features=['pickup_community_area','dropoff_community_area'],
        numerical_features=[])

    # Transform
    X_train, X_val, y_train, y_val, dv = build_model(df_train,y_train, df_val,y_val)

    # Train
    train_best_model(X_train, X_val, y_train, y_val, dv)


if __name__ == "__main__":
    main_flow()