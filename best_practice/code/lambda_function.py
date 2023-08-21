import model
import os




PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'chicago-ride-predictions')
# RUN_ID = 'a6203da436864c7ea7d2ce768f2ec697'
RUN_ID = os.getenv('RUN_ID')
TEST_RUN = os.getenv('DRY_RUN','False') == 'True'

model_service = model.init(
    prediction_stream_name=PREDICTIONS_STREAM_NAME,
    run_id=RUN_ID,
    test_run=TEST_RUN,
)

def lambda_handler(event, context):
    return model_service.lambda_handler(event)