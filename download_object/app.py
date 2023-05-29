import json
import os
import boto3
from botocore.exceptions import ClientError


s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DennisCmIndex')


def lambda_handler(event, context):
    qs_params = event['queryStringParameters']
    url = create_presigned_url(qs_params['object-key'])

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps({
            "message": {
                "url": url,
                "count": 0
            }
        }),
    }


def create_presigned_url(object_name, expiration=3600):
    bucket_name = os.environ['BUCKET_NAME']

    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
    except ClientError as e:
        raise Exception(e)

    return url
