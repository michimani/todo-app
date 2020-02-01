from chalice import Chalice, Response
from chalicelib import db
import time
import json

app = Chalice(app_name='todo-app')
dynamo = db.get_db()


@app.route('/todo', methods=['GET'])
def get_todo():
    todos = dynamo.scan()
    return return_response(todos['Items'], 200)


@app.route('/todo/{todo_id}', methods=['DELETE'])
def delete_todo(todo_id):
    dynamo.delete_item(Key={'Id': str(todo_id)})
    return return_response({}, 200)


@app.route('/todo', methods=['PUT'])
def add_todo():
    todo_id = str(time.time()).replace('.', '')
    req_body = get_bosy_as_dict()

    if 'title' not in req_body:
        return return_response({
            'message': 'key error: the following parameter is required: title',
        }, 400)

    try:
        new_todo = {
            'Id': todo_id,
            'Title': req_body['title'],
            'Done': '0'
        }

        if 'content' in req_body:
            new_todo['Content'] = req_body['content']

        res = dynamo.put_item(Item=new_todo,
                              ConditionExpression='attribute_not_exists(Id)')

        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            return return_response({
                'message': 'Failed to add a todo.',
                'response_from_dynamodb': res
            }, res['ResponseMetadata']['HTTPStatusCode'])

        return return_response({
            'added_todo_id': new_todo['Id'],
        }, 200)
    except Exception as e:
        return return_response({
            'message': str(e)
        }, 500)


def get_bosy_as_dict():
    return json.loads(app.current_request.raw_body.decode('utf-8'))


def return_response(body, code):
    return Response(body=body,
                    status_code=code,
                    headers={'Content-Type': 'application/json'})
