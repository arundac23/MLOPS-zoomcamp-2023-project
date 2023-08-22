import json
import boto3
import base64
import os
import mlflow





kinesis_client = boto3.client('kinesis')

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'chicago-ride-predictions')

RUN_ID = 'a6203da436864c7ea7d2ce768f2ec697'
logged_model = f's3://mlflow-artifact-remote-chicago-taxi-prediction/1/{RUN_ID}/artifacts/models'
model = mlflow.pyfunc.load_model(logged_model)

TEST_RUN = os.getenv('DRY_RUN','False') == 'True'

def prepare_features(ride):
    features = {}
    features['pickup_community_area'] = ride['pickup_community_area'],
    features['dropoff_community_area'] = ride['dropoff_community_area']
    return features
    
def predict(features):
    pred= model.predict(features)
    return float(pred [0])
    
def lambda_handler(event, context):

    
    #print(json.dumps(event))
    
    prediction_events = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)
        #print(ride_event)
        ride = ride_event['ride']
        ride_id = ride_event['ride_id']
        features=prepare_features(ride)
        prediction = predict(features)
        prediction_event = {
            'model':'chicago-ride-duration-prediction-model',
            'version': '004',
            'prediction' :{
                'ride_duration': prediction,
                'ride_id' : ride_id
            }
        }
        if not TEST_RUN:
            kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey=str(ride_id),
            )
        prediction_events.append(prediction_event)
    return {
        'predictions':prediction_events
    }