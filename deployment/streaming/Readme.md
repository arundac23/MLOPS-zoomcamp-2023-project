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


### bash
export PREDICTIONS_STREAM_NAME = 'chicago-ride-predictions'
export TEST_RUN = 'True'

python test.py


### Docker 

docker build -t stream-model-chicago-taxi-duration:v1 .

docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="chicago-ride-predictions" \
    -e TEST_RUN="True" \
    -e AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE" \
    -e AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
    -e AWS_DEFAULT_REGION="us-east-2" \
    stream-model-chicago-taxi-duration:v1

### url for testing the docker
* http://localhost:8080/2015-03-31/functions/function/invocations

### Creating an ECR repo

aws ecr create-repository --repository-name chicago-taxi-duration-model

bash
$(aws ecr get-login --no-include-email)

REMOTE_URI="150675264512.dkr.ecr.us-east-2.amazonaws.com/chicago-taxi-duration-model"
REMOTE_TAG="v1"
REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}

LOCAL_IMAGE="stream-model-chicago-taxi-duration:v1"
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE} 

docker push 150675264512.dkr.ecr.us-east-2.amazonaws.com/chicago-taxi-duration-model:v1