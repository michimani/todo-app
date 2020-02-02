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


def scan_todo():
    db = get_db()
    return db.scan()


def get_todo(todo_id):
    db = get_db()
    return db.get_item(Key={'Id': todo_id})


def put_todo(todo_data):
    db = get_db()
    return db.put_item(
        Item=todo_data, ConditionExpression='attribute_not_exists(Id)')


def delete_todo(todo_id):
    db = get_db()
    return db.delete_item(Key={'Id': todo_id})
