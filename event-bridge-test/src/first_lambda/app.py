from datetime import datetime, timedelta, timezone
import boto3
import os
import random
import time

scheduler_client = boto3.client('scheduler')

def lambda_handler(event, context):
    # 50% chance to create a delayed invocation of SecondLambdaFunction
    if random.random() < 0.5:
        schedule_role_arn = os.getenv('SCHEDULE_ROLE_ARN')
        second_lambda_arn = os.getenv('SECOND_LAMBDA_ARN')
        
        # Generate unique name for the schedule
        schedule_name = f"second_lambda_invocation_{int(time.time())}"
        
        # Set the invocation time with required format
        # Create the schedule
        response = scheduler_client.create_schedule(
            Name=schedule_name,
            ScheduleExpression="rate(1 minute)",
            Target={
                'Arn': second_lambda_arn,
                'RoleArn': schedule_role_arn,
            },
            FlexibleTimeWindow={
                'Mode': 'OFF'
            }
        )
        
        return {
            'statusCode': 200,
            'body': f'Schedule created for SecondLambdaFunction with 1 min delay.'
        }
    
    return {
        'statusCode': 200,
        'body': 'No schedule created this time.'
    }
