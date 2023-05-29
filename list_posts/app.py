import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DennisCmIndex')


def lambda_handler(event, context):
    r = table.scan()
    items = r['Items']
    print(f'NUMBER OF ITEMS: {len(items)}')

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
