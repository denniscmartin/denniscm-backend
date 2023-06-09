import boto3
import json


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GithubPublicRepos')


def lambda_handler(event, context):
    event_msg = event['body']['message']

    with table.batch_writer() as batch:

        # pk -> repo name
        # sk -> repo id

        for repo in event_msg['repos']:
            batch.put_item(
                Item={
                    'pk': repo['name'],
                    'sk': str(repo['id']),
                    'description': repo['description'],
                    'url': repo['url']
                }
            )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "ok"
        })
    }
