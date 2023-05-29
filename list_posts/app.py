import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DennisCmIndex')


def lambda_handler(event, context):
    r = table.scan(
        FilterExpression=Key('item_name').begins_with('post::')
    )

    items = r['Items']

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps({
            "message": {
                "items": items,
                "count": len(items)
            }
        }),
    }
