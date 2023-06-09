import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GithubPublicRepos')


def lambda_handler(event, context):
    reponse = table.scan()

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps({
            "message": {
                "repos": reponse['Items'],
                "count": len(reponse['Items'])
            }
        })
    }
