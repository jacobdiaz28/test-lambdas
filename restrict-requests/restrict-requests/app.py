import os
import requests
import socket

def lambda_handler(event, context):
    # Initialize response data
    response_data = {}

    # Perform nslookup for www.google.com
    try:
        acteln_ip = socket.gethostbyname('test.acteln.com')
    except socket.gaierror as e:
        acteln_ip = str(e)
    response_data['acteln_ip'] = acteln_ip

    # Perform nslookup for www.yahoo.com
    try:
        yahoo_ip = socket.gethostbyname('www.yahoo.com')
    except socket.gaierror as e:
        yahoo_ip = str(e)
    response_data['yahoo_ip'] = yahoo_ip

    # Attempt to access allowed domain with a 5-second timeout
    try:
        acteln_response = requests.get('http://test.acteln.com', timeout=5)
        acteln_status = acteln_response.status_code
    except requests.exceptions.RequestException as e:
        acteln_status = str(e)  # Likely to fail due to restriction or timeout
    
    # Attempt to access restricted domain with a 5-second timeout
    try:
        yahoo_response = requests.get('https://www.yahoo.com', timeout=5)
        yahoo_status = yahoo_response.status_code
    except requests.exceptions.RequestException as e:
        yahoo_status = str(e)  # Likely to fail due to restriction or timeout

    # Add the status codes to the response data
    response_data['acteln_status'] = acteln_status
    response_data['yahoo_status'] = yahoo_status

    return {
        'statusCode': 200,
        'body': response_data
    }
