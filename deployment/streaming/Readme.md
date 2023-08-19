{
    "ride": {
        "pickup_community_area" : 6,
        "dropoff_community_area" : 32
    },
    "ride_id": 123
}

`KINESIS_STREAM_INPUT=ride_events
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data "Hello, this is a test."`

Decoding base64

`base64.b64decode(data_encoded).decode('utf-8')`