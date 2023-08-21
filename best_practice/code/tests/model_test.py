from pathlib import Path

import model


def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, 'rt', encoding='utf-8') as f_in:
        return f_in.read().strip()


def test_base64_decode():
    base64_input = read_text('data.b64')

    actual_result = model.base64_decode(base64_input)
    expected_result = {'model': 'chicago-ride-duration-prediction-model', 'version': '1223', 'prediction': {'ride_duration': 20.928277928045613, 'ride_id': 13579}}
    assert actual_result == expected_result


def test_prepare_features():
    model_service = model.ModelService(None)

    ride = {
        "pickup_community_area": "6",
        "dropoff_community_area": "32",
    }

    actual_features = model_service.prepare_features(ride)

    expected_fetures = {
        "pickup_community_area": "6",
        "dropoff_community_area": "32",
    }

    assert actual_features == expected_fetures


class ModelMock:
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n


def test_predict():
    model_mock = ModelMock(10.0)
    model_service = model.ModelService(model_mock)

    features = {
        "pickup_community_area": "6",
        "dropoff_community_area": "32",
    }

    actual_prediction = model_service.predict(features)
    expected_prediction = 10.0

    assert actual_prediction == expected_prediction