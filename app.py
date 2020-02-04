from chalice import Chalice, Response
from chalicelib import db
import time
import json
import boto3

app = Chalice(app_name='todo-app')


@app.route('/todos', methods=['GET'], api_key_required=True)
def list_todo():
    todos = db.scan_todo()
    return return_response(todos['Items'], 200)


@app.route('/todos/{todo_id}', methods=['GET'], api_key_required=True)
def get_todo(todo_id):
    res = db.get_todo(todo_id)

    if 'Item' not in res:
        return return_response({
            'message': 'not found error: todo with Id = {todo_id} was not found'
            .format(todo_id=todo_id)
        }, 404)

    return return_response(res['Item'], 200)


@app.route('/todos/{todo_id}', methods=['DELETE'], api_key_required=True)
def delete_todo(todo_id):
    db.delete_todo(todo_id)
    return return_response({}, 200)


@app.route('/todos', methods=['POST'], api_key_required=True)
def add_todo():
    todo_id = str(time.time()).replace('.', '')
    req_body = get_bosy_as_dict()

    if 'title' not in req_body:
        return return_response({
            'message': 'key error: the following parameter is required: title',
        }, 400)

    try:
        new_todo = {
            'todo_id': todo_id,
            'title': req_body['title'],
            'done': '0'
        }

        if 'content' in req_body:
            new_todo['content'] = req_body['content']

        res = db.put_todo(new_todo)

        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            return return_response({
                'message': 'Failed to add a todo.',
                'response_from_dynamodb': res
            }, res['ResponseMetadata']['HTTPStatusCode'])

        return return_response({
            'added_todo_id': new_todo['todo_id'],
        }, 200)
    except Exception as e:
        return return_response({
            'message': str(e)
        }, 500)


@app.route('/dummy', methods=['GET'], api_key_required=True)
def dummy():
    client_db = boto3.client('dynamodb')
    table_name = db.get_table_name()
    client_db.scan(TableName=table_name)
    client_db.put_item(TableName=table_name, Item={
                       'todo_id': {'S': '0'}, 'title': {'S': 'dummy'}})
    client_db.get_item(TableName=table_name, Key={'todo_id': '0'})
    client_db.delete_item(TableName=table_name, Key={'todo_id': '0'})
    return return_response({'message', 'This is dummy api'}, 200)


def get_bosy_as_dict():
    return json.loads(app.current_request.raw_body.decode('utf-8'))


def return_response(body, code):
    return Response(body=body,
                    status_code=code,
                    headers={'Content-Type': 'application/json'})
