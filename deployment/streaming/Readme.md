### Record example
{
    "ride": {
        "pickup_community_area" : 6,
        "dropoff_community_area" : 32
    },
    "ride_id": 123
}

KINESIS_STREAM_INPUT=chicago-ride-predictions
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data "Hello, this is a test."

#### Decoding base64

`base64.b64decode(data_encoded).decode('utf-8')`

### Sending this record
KINESIS_STREAM_INPUT=chicago-ride-predictions

aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data '{
        "ride": {
            "pickup_community_area": "6",
            "dropoff_community_area": "32"
        }, 
        "ride_id": 13579
    }'

### Reading from the stream

KINESIS_STREAM_OUTPUT='chicago-ride-predictions'
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis \
    get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator' \
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode | jq


``` bash
export PREDICTIONS_STREAM_NAME = 'chicago-ride-predictions'
export TEST_RUN = 'True'
python test.py
    ``````

### Docker 

docker build -t stream-model-chicago-taxi-duration:v2 .

docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="chicago-ride-predictions" \
    -e TEST_RUN="True" \
    -e AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE" \
    -e AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
    -e AWS_DEFAULT_REGION="us-east-2" \
    stream-model-chicago-taxi-duration:v1

RUN_ID = 'a6203da436864c7ea7d2ce768f2ec697

docker build -t stream-model-chicago-taxi-duration:v2 .

docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="chicago-ride-predictions" \
    -e RUN_ID="a6203da436864c7ea7d2ce768f2ec697" \
    -e TEST_RUN="True" \
    -e AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE" \
    -e AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
    -e AWS_DEFAULT_REGION="us-east-2" \
    stream-model-chicago-taxi-duration:v3

### url for testing the docker
* http://localhost:8080/2015-03-31/functions/function/invocations

### Creating an ECR repo

aws ecr create-repository --repository-name chicago-taxi-duration

bash
$(aws ecr get-login --no-include-email)

REMOTE_URI="150675264512.dkr.ecr.us-east-2.amazonaws.com/chicago-taxi-duration"
REMOTE_TAG="v3"
REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}

LOCAL_IMAGE="stream-model-chicago-taxi-duration:v3"
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE} 

docker push 150675264512.dkr.ecr.us-east-2.amazonaws.com/chicago-taxi-duration-model:v1




{
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "13579",
                "sequenceNumber": "49643835789842723091234810043917548543000268625363861506",
                "data": "eyJtb2RlbCI6ICJjaGljYWdvLXJpZGUtZHVyYXRpb24tcHJlZGljdGlvbi1tb2RlbCIsICJ2ZXJzaW9uIjogIjEyMjMiLCAicHJlZGljdGlvbiI6IHsicmlkZV9kdXJhdGlvbiI6IDIwLjkyODI3NzkyODA0NTYxMywgInJpZGVfaWQiOiAxMzU3OX19",
                "approximateArrivalTimestamp": 1692708559.02
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49643835789842723091234810043917548543000268625363861506",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::150675264512:role/lambda-kinesis-role",
            "awsRegion": "us-east-2",
            "eventSourceARN": "arn:aws:kinesis:us-east-2:150675264512:stream/chicago-ride-predictions"
        }
    ]
}


old:

{
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
