def lambda_handler(event, context):
    # Perform the task for the second Lambda
    print("Second Lambda function executed after 30-second delay.")
    print(f"Received event: {event}")
