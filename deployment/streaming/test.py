import lambda_function

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

result = lambda_function.lambda_handler(event, None)
print(f'Result : {result}')