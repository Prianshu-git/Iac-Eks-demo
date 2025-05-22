import boto3
import os

def get_secret():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    secret = client.get_secret_value(SecretId='flaskapp/secret')
    return secret['SecretString']

os.environ['APP_SECRET'] = get_secret()