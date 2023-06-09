import requests


url = f'https://api.github.com/users/denniscmartin/repos'
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'X-GitHub-Api-Version': "2022-11-28"
}


def lambda_handler(event, context):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f'Request to Github failed with status code {response.text}.')

    repos = []
    for repo in response.json():
        if repo['description']:
            repos.append({
                'id': repo['id'],
                'name': repo['name'],
                'description': repo['description'],
                'url': repo['url']
            })

    return {
        "statusCode": 200,
        "body": {
            "message": {
                "repos": repos
            }
        },
    }
