import os
import boto3


def get_db():
    endpoint = os.environ.get('DB_ENDPOINT')
    table_name = os.environ.get('DB_TABLE_NAME')

    if endpoint:
        resource = boto3.resource('dynamodb', endpoint_url=endpoint)
    else:
        resource = boto3.resource('dynamodb')

    return resource.Table(table_name)
