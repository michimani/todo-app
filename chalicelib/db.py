import os
import boto3

endpoint = os.environ.get('DB_ENDPOINT')
table_name = os.environ.get('DB_TABLE_NAME')


def get_db():
    if endpoint:
        resource = boto3.resource('dynamodb', endpoint_url=endpoint)
    else:
        resource = boto3.resource('dynamodb')

    return resource.Table(table_name)


def get_table_name():
    return table_name


def scan_todo():
    db = get_db()
    return db.scan()


def get_todo(todo_id):
    db = get_db()
    return db.get_item(Key={'todo_id': todo_id})


def put_todo(todo_data):
    db = get_db()
    return db.put_item(
        Item=todo_data, ConditionExpression='attribute_not_exists(todo_id)')


def delete_todo(todo_id):
    db = get_db()
    return db.delete_item(Key={'todo_id': todo_id})
