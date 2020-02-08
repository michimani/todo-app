from boto3.dynamodb.conditions import Key, Attr
import boto3
import os

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


def get_todos(user_id):
    db = get_db()
    return db.query(
        KeyConditionExpression=Key('user_id').eq(user_id))


def get_todos_with_done(user_id, done):
    db = get_db()
    return db.query(
        IndexName='FilterDoneIndex',
        KeyConditionExpression=Key('user_id').eq(user_id) &
        Key('l_idx_done').begins_with(done + '#')
    )


def get_todo(user_id, todo_id):
    db = get_db()
    return db.get_item(Key={'user_id': user_id, 'todo_id': todo_id})


def update_todo(user_id, todo_id, patch_data):
    current_todo_res = get_todo(user_id, todo_id)
    if current_todo_res['ResponseMetadata']['HTTPStatusCode'] != 200:
        return current_todo_res

    target_todo = current_todo_res['Item']
    target_todo.update(patch_data)
    db = get_db()
    return db.put_item(Item=target_todo)


def put_todo(todo_data):
    db = get_db()
    return db.put_item(
        Item=todo_data, ConditionExpression=Attr('todo_id').not_exists())


def delete_todo(user_id, todo_id):
    db = get_db()
    return db.delete_item(Key={'user_id': user_id, 'todo_id': todo_id},
                          ReturnValues='ALL_OLD')
