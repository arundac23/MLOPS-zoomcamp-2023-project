import os
import pickle

import mlflow
from flask import Flask, request, jsonify


# RUN_ID = os.getenv('RUN_ID')
RUN_ID = 'a6203da436864c7ea7d2ce768f2ec697'
logged_model = f's3://mlflow-artifact-remote-chicago-taxi-prediction/1/{RUN_ID}/artifacts/models'
# logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)


def prepare_features(ride):
    features = {}
    features['pickup_community_area'] = ride['pickup_community_area'],
    features['dropoff_community_area'] = ride['dropoff_community_area']
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds[0])


app = Flask('chicago-taxi-duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)