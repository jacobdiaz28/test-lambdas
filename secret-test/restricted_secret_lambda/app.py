import os
import json
import boto3
from botocore.exceptions import ClientError

# Initialize the Secrets Manager client
secrets_client = boto3.client('secretsmanager')

def get_secret(secret_name):
    """
    Attempts to retrieve a secret from AWS Secrets Manager.
    """
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        # Secrets Manager returns the secret value as a JSON string
        if 'SecretString' in response:
            return json.loads(response['SecretString'])
        else:
            raise Exception("SecretString not found in the response")
    except ClientError as e:
        print(f"Access to secret '{secret_name}' failed: {e}")
        return f"Access to secret '{secret_name}' failed: {str(e)}"

def lambda_handler(event, context):
    # Retrieve the authorized secret name from environment variables
    authorized_secret_name = os.environ['SECRET_NAME']
    
    # Fetch the authorized secret
    authorized_secret = get_secret(authorized_secret_name)
    
    # Attempt to retrieve the unauthorized secret
    unauthorized_secret_name = "SomeOtherSecret"
    unauthorized_secret = get_secret(unauthorized_secret_name)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "authorized_secret": authorized_secret,
            "unauthorized_secret": unauthorized_secret
        })
    }
