import os
import boto3

# Initialize clients for AWS services
ssm_client = boto3.client('ssm')

def get_parameter_value(name):
    """
    Fetches the parameter value from SSM Parameter Store.
    """
    try:
        response = ssm_client.get_parameter(Name=name)
        return response['Parameter']['Value']
    except ssm_client.exceptions.ParameterNotFound:
        return f"Parameter {name} not found."

def lambda_handler(event, context):
    # Retrieve SSM Parameters by their names
    apple_value = get_parameter_value("apple")
    banana_value = get_parameter_value("Banana")
    cherry_value = get_parameter_value("Cherry")
    dragonfruit_value = get_parameter_value("Dragonfruit")
    elderberry_value = get_parameter_value("Elderberry")

    # Retrieve Parameters set via CloudFormation Parameters section
    dish_value = os.environ.get("dish", "Cake")  # Defaults to "Cake"
    elderberry_dish_value = os.environ.get("elderberryDish", "pudding")  # Defaults to "pudding"

    # Log or return all retrieved values
    result = {
        "apple": apple_value,
        "banana": banana_value,
        "cherry": cherry_value,
        "dragonfruit": dragonfruit_value,
        "elderberry": elderberry_value,
        "dish": dish_value,
        "elderberryDish": elderberry_dish_value,
    }

    print("Retrieved parameters:", result)  # Logging for debugging

    # Return the values in response
    return {
        "statusCode": 200,
        "body": result
    }
