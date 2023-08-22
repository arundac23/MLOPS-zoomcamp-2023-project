# MLOPS-zoom camp-2023-project - Chicago Taxi Ride prediction
The final project of MLOPS Zoomcamp 2023

This project involves model development, tracking, deployment, and monitoring machine learning models using MLops best practices. The following tasks are involved in the full completion of this project.
- Basic machine learning model development.
- Experiment tracking and model registry (MLFLOW)
- Workflow orchestration(PREFECT)
- Containerization(DOCKER)
- Cloud computing(AWS)
- Model monitoring(EVIDENTLY)
- best practices: code quality, code tests, pre-commit, make file
- Infrastructure as Code(TERRAFORM) --> Pending
- Continuous integration, continuous deployment, and continuous training --> pending

## 1. PROBLEM DESCRIPTION:
The dataset used in this project is relatively simple and similar to the course content. Since I don't have much time to build a complex model. My primary focus is to understand the MLOps procedure and principles. I selected the Chicago Taxi Trips dataset to forecast trip durations, accessible at https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew.

This dataset is not available as individual files. The About link contains the entire dataset of Chicago taxi rides. The code in the jupyter file `location/development/notebook.ipynb` will read the link and split that into three individual `CSV` files. The split is based on the year and month of that ride. It also converts `CSV` files into `parquet` after some initial cleanup.

The target parameter for the project is time `duration`.  Due to time limitations, I didn't spend time improving the accuracy of the models. I just did some basic parameter tuning for all the models before selecting the final model.

My goal is to implement a maturity level of up to 4. But I am not able to complete all tasks at this time due to my other commitments. I will continue this project to improve the model's performance and  maturity level of it.

## 2. CLOUD SERVICE:
In this project, I used AWS `EC2` for virtual machines, `S3` bucket for storing the `mlflow` models, and `Postgresql` `RDS` for `mlflow` experiments tracking. In addition to this, I used AWS lambda and kinesis for my streaming deployment.
### AWS account creation:
Use any email id to create an account. 
After account creation, select your related region. You need to use the same region for all the VM instances and other integrated services.
### IAM update
Open the IAM features and click user
Create the new user
add permission policy to access the required services
Generate the AWS key and also the AWS secret key. This is important for aws cli configuration. Please store that information.
### Creation of EC2 instance:
For the model tracking server, the default option with a free tier instance type is enough. For model deployment high configuration instance type and more storage option is required. This may incur some costs. 
For the EC2 instance, key pair needs to be generated and downloaded. It should be stored in your local .ssh folder.
For mlflow server, an additional security group is required as mentioned in the course with a port of 5000.

![image](https://github.com/arundac23/MLOPS-zoomcamp-2023-project/assets/76126029/f41ec5ad-92d4-4e08-82cf-f41d5e5f60fd)

once instance was created. Start and connect the instance through AWS Linux or Ubuntu.
### S3 Bucket:
This is cloud storage for ML flow models and artifacts.
* Open the s3 
* Create the new bucket
* Write your s3 bucket name and save it for easy reference.
* Make sure the timezone is the same as your other services.
* All default settings should be ok.
* Add required permission policy to access and store the data in S3

### RDS database:
* Create a database in RDS.
* Select Postgresql as the database.
* select the free tier
* provide DB instance identifier
* provide the master username.
* Select Auto-generate a password --> But you need to save a password that will be generated while creating the database.
* Create a database.
* Note: EC2 security instance needs to be added to this RDS security group. This will connect both the server and the database.

## 3. MLFLOW EXPERIMENT TRACKING AND MODEL REGISTRY:
The `experiment_tracking` Folder contains two jupyter files `notebook_mlflow_local.ipynb` and `notebook_AWS_cloud.ipynb`. 
One is tracked and saved the model locally and another is tracked in the AWS server and saved in the S3 bucket.

#### For local tracking:
Create a conda environment and install the required libraries.

tracking uri is sqlite:///mlflow.db. 

Run the mlflow UI.
 ```bash
   mlflow ui --backend-store-URI sqlite:///mlflow.db
   ```
open local host port.
 ```bash
   localhost:5000
   ```
Then run the `notebook_mlflow_local.ipynb` in a separate terminal or through VS code with a remote connection.
All the experiments logs, artifacts, and models will tracked and saved in the database.

Through ML flow client model was registered and moved to stage or production.
#### AWS Tracking: 
* Through AWS Linux or ubuntu.
* configure your AWS credentials through AWS CLI.
Then run this aws terminal
* ```bash
   mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://{Master user name}:6XPj1FLSf5vVIdXnc6Pk@{END POINT}:5432/{initial database name} --default-artifact-root s3://{S3 bucket name}
   ```
And model tracking can be seen in the server host.
example: `"http://ec2-18-222-108-158.us-east-2.compute.amazonaws.com:5000"` This will vary based on each server instance.

Then run the `notebook_AWS_cloud.ipynb` in a separate terminal --> Make sure you change the server host and add the necessary permission policy to S3 for saving and tracking the mlflow models.
## 4. Workflow Orchestration:
Prefect is used for Workflow Orchestration. Xgboost from MLflow registry model is used for this workflow orchestration and deployment. 
The Jupyter notebook from the Mlflow model is converted into an executable Python file `prefect_orchestration.py`. 
Python decorators like task and flow were added to monitor the workflow.

Create a conda env and pip install required packages using `pip install -r requirements.txt`

Run a prefect server in terminal

 ```bash
 prefect server start
   ```

Check the flow in localhost port
 ```bash
 localhost:8080
   ```
Run `python prefect_orchestration.py` in a separate terminal

Initialize the prefect project
```bash
prefect project init
   ```
This will generate `prefect.yaml`, `deployment.yaml`, `.prefectignore`, 

Create a workpool in a prefect UI and deploy using this command in terminal

```bash
prefect deploy <path to the model location >:main_flow -n <model_name> -p <workpool_name>
   ```
Then Run the worker network
```bash
prefect worker start
   ```
Before running the prefect deployment, make sure all the files are pushed in remote locations.

Open the Prefect UI and find the flows. Click quick run.

You can see generated data in the terminal while running the flow. You can schedule this flow with different interval in prefect UI.

## 5. Model Deployment:
### Web-Service Deployment:
I just deployed the web service model locally. I didn't deploy it in AWS server. Since I used AWS cloud for streaming deployment.
`predict.py` python model was created for the deployment.

Mlflow production model is saved in S3 bucket. It can be retrieved directly based on its run id.

```bash
RUN_ID = 'a6203da436864c7ea7d2ce768f2ec697'
logged_model = f's3://mlflow-artifact-remote-chicago-taxi-prediction/1/{RUN_ID}/artifacts/models'
model = mlflow.pyfunc.load_model(logged_model)
   ```

#### Feature engineering and prediction function
```bash
def prepare_features(ride):
    features = {}
    features['pickup_community_area'] = ride['pickup_community_area'],
    features['dropoff_community_area'] = ride['dropoff_community_area']
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds[0])
   ```
#### Flask API and connecting port
```bash
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
   ```

Create pipenv env with required packages

Run `python predict.py`

Run `python test.py` in a separate terminal to see the prediction.

### Streaming Deployment:
Deployment in a streaming context involves the real-time distribution and execution of applications or models. It is particularly relevant in scenarios where data arrives continuously and needs to be processed in a timely manner. In the realm of machine learning, stream deployment could refer to deploying machine learning models that make predictions on incoming data streams in real-time

In this project, we will use kinesis to handle streaming data and lambda to process and transform the data.

First set up AWS lambda function and kinesis data stream and select provisioned option in Amazon web service.
create a role and add permission for AWSLambdaKinesisExectuionRole 
Create a lambda function and assign the role to it. Create a data stream using Amazon Kinesis. Add kinesis as a trigger to the lambda function.
After the trigger is enabled, then we can run this following command as test in the terminal:
```bash
{ "ride": { "pickup_community_area" : 6, "dropoff_community_area" : 32 }, "ride_id": 123 }

KINESIS_STREAM_INPUT=chicago-ride-predictions aws kinesis put-record
--stream-name ${KINESIS_STREAM_INPUT}
--partition-key 1
--data "Hello, this is a test."
   ```
Then check the streaming data in the cloudwatch

Include this `base64.b64decode(data_encoded).decode('utf-8')` in lambda function to decode the data stream into readable format.

```bash
def lambda_handler(event, context):

    
    print(json.dumps(event))
    
    prediction_events = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)
        print(ride_event)
        ride = ride_event['ride']
        ride_id = ride_event['ride_id']
        features=prepare_features(ride)
        prediction = predict(features)
        prediction_event = {
            'model':'chicago-ride-duration-prediction-model',
            'version': '1223',
            'prediction' :{
                'ride_duration': prediction,
                'ride_id' : ride_id
            }
        }
   ```

As we develop further, we refine the input to the data stream
```bash
KINESIS_STREAM_INPUT=chicago-ride-predictions

aws kinesis put-record
--stream-name ${KINESIS_STREAM_INPUT}
--partition-key 1
--data '{ "ride": { "pickup_community_area": "6", "dropoff_community_area": "32" }, "ride_id": 13579 }
   ```

Record of the stream data will available in cloud watch as JSON format
```bash
event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49643747291208665319133457446498095704868846562692825090",
                "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAicGlja3VwX2NvbW11bml0eV9hcmVhIjogIjYiLAogICAgICAgICAgICAiZHJvcG9mZl9jb21tdW5pdHlfYXJlYSI6ICIzMiIKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDEyMzQ1NgogICAgfQ==",
                "approximateArrivalTimestamp": 1692503185.509
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49643747291208665319133457446498095704868846562692825090",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::150675264512:role/lambda-kinesis-role",
            "awsRegion": "us-east-2",
            "eventSourceARN": "arn:aws:kinesis:us-east-2:150675264512:stream/ride-events"
        }
    ]
}
   ```
#### Finally reading the result from a stream:
```bash
KINESIS_STREAM_OUTPUT='chicago-ride-predictions' SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis
get-shard-iterator
--shard-id ${SHARD}
--shard-iterator-type TRIM_HORIZON
--stream-name ${KINESIS_STREAM_OUTPUT}
--query 'ShardIterator'
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode | jq
   ```

### Run a test using `test.py` in a terminal
```bash
export PREDICTIONS_STREAM_NAME = 'chicago-ride-predictions' export TEST_RUN = 'True'

python test.py in a separate terminal
   ```
build a docker container using Dockerfile and pipenv files
```bash
docker build -t stream-model-chicago-taxi-duration:v1 .
   ```
Run the docker container
``` bash
docker run -it --rm
-p 8080:8080
-e PREDICTIONS_STREAM_NAME="chicago-ride-predictions"
-e TEST_RUN="True"
-e AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
-e AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
-e AWS_DEFAULT_REGION="us-east-2"
stream-model-chicago-taxi-duration:v1
   ```
Use `test_docker.py` to check the prediction.

Finally, create a repository in AWS ECR using aws cli

```bash
aws ecr create-repository --repository-name chicago-taxi-duration-model
   ```
```bash
$(aws ecr get-login --no-include-email)
   ```
```bash
REMOTE_URI="150675264512.dkr.ecr.us-east-2.amazonaws.com/chicago-taxi-duration-model"
REMOTE_TAG="v1"
REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}

LOCAL_IMAGE="stream-model-chicago-taxi-duration:v1"
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE}
   ```
Then create a new lambda using this elastic container. Then, we create the policy for our s3 as services and include the list and read permission.
Use the shard iterator again to specify the position to start reading the stream.
