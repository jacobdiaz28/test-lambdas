import os
import boto3

sns = boto3.client('sns')
topic_arn = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    message = "Hello from Lambda!"
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message
    )
    return {
        "statusCode": 200,
        "body": f"Message sent to SNS topic {topic_arn}"
    }
