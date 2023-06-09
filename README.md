# denniscm-backend

## Important
Before deploying the app, create an AWS Secret

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Github token for denniscmartin

Resources:
    GithubSecret:
        Type: AWS::SecretsManager::Secret
        Properties:
            Name: DennisCMartinGithubSecret
            Description: Github token to use the API
            SecretString: '{"token":"token-here"}'
            
Outputs:
    GithubSecretArn:
        Description: Github token for denniscmartin
        Value: !Ref GithubSecret
        Export:
            Name: DennisCMartinGithubSecretArn
```