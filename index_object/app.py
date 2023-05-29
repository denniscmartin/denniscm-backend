import json
import boto3
import uuid
from datetime import date


s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
dynamo_table = dynamodb.Table('DennisCmIndex')


def lambda_handler(event, context):
    for record in event['Records']:
        s3_metadata = record['s3']
        s3_bucket_name = s3_metadata['bucket']['name']
        s3_object_key = s3_metadata['object']['key']

        if s3_object_key == 'inbox/':
            print('Folder created, ignoring event')
        else:
            file_ext = s3_object_key.split('.', 1)[1]
            s3_new_object_key = f'indexed/{uuid.uuid4()}.{file_ext}'

            print(f'Renaming object to: {s3_new_object_key}')

            r_copy = s3_client.copy_object(
                Bucket=s3_bucket_name,
                CopySource=f'{s3_bucket_name}/{s3_object_key}',
                Key=s3_new_object_key
            )

            if r_copy['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise Exception(r_copy)

            print('Deleting old object')

            r_delete = s3_client.delete_object(
                Bucket=s3_bucket_name,
                Key=s3_object_key
            )

            if r_delete['ResponseMetadata']['HTTPStatusCode'] != 204:
                raise Exception(r_delete)

            print('Indexing object')

            filename = s3_object_key.split('/', 1)[1]
            if file_ext == 'txt':
                filename = f'post::{filename}'
            else:
                filename = f'image::{filename}'

            created_at = str(date.today())
            dynamo_table.put_item(
                Item={
                    'item_key': s3_new_object_key,
                    'item_name': filename,
                    'created_at': created_at
                }
            )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "ok",
        }),
    }
