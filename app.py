from chalice import Chalice, Response
from chalicelib import db
import time
import json
import hashlib

app = Chalice(app_name='todo-app')


@app.route('/todos', methods=['GET'], api_key_required=True)
def get_todos():
    user_id = get_user_id()
    query_params = get_query_params()
    todos = db.get_todos(user_id)

    filtered_todos = filter_todos(todos['Items'], query_params)
    return return_response(filtered_todos, 200)


@app.route('/todos/{todo_id}', methods=['GET'], api_key_required=True)
def get_todo(todo_id):
    user_id = get_user_id()
    res = db.get_todo(user_id, todo_id)

    if 'Item' not in res:
        return return_response({
            'message': ('not found error: todo with '
                        'Id = {todo_id} was not found').format(todo_id=todo_id)
        }, 404)

    return return_response(res['Item'], 200)


@app.route('/todos/{todo_id}', methods=['PATCH'], api_key_required=True)
def update_todo(todo_id):
    user_id = get_user_id()
    params = get_bosy_as_dict()

    if 'title' not in params \
            and 'content' not in params \
            and 'done' not in params:
        return return_response({
            'message': ('parameter error: one of the following parameters '
                        'is required: title, content, done'),
        }, 400)

    if ('title' in params and params['title'] == '') \
            or ('done' in params and str(params['done']) not in ['0', '1']):
        return return_response({
            'message': ('parameter error: invalid value for '
                        'one of the following parameters '
                        'is required: title, done'),
        }, 400)

    patch_data = {}
    if 'title' in params:
        patch_data['title'] = params['title']

    if 'content' in params:
        patch_data['content'] = params['content']

    if 'done' in params:
        patch_data['done'] = str(params['done'])

    try:
        res = db.update_todo(user_id, todo_id, patch_data)

        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            return return_response({
                'message': 'Failed to update a todo.',
                'response_from_dynamodb': res
            }, res['ResponseMetadata']['HTTPStatusCode'])

        return return_response({
            'update_todo_id': todo_id,
        }, 200)
    except Exception as e:
        return return_response({
            'message': str(e)
        }, 500)


@app.route('/todos/{todo_id}', methods=['DELETE'], api_key_required=True)
def delete_todo(todo_id):
    user_id = get_user_id()
    db.delete_todo(user_id, todo_id)
    return return_response({}, 200)


@app.route('/todos', methods=['POST'], api_key_required=True)
def add_todo():
    user_id = get_user_id()
    todo_id = str(time.time()).replace('.', '')
    req_body = get_bosy_as_dict()

    if 'title' not in req_body:
        return return_response({
            'message': 'key error: the following parameter is required: title',
        }, 400)

    try:
        new_todo = {
            'user_id': user_id,
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


def get_user_id():
    return hashlib.sha1(
        app.current_request.headers['x-api-key'].encode('utf-8')).hexdigest()


def get_query_params():
    query_params = dict()

    request_dict = app.current_request.to_dict()
    if request_dict['query_params'] is not None:
        query_params = request_dict['query_params']

    return query_params


def get_bosy_as_dict():
    try:
        return json.loads(app.current_request.raw_body.decode('utf-8'))
    except Exception:
        return {}


def filter_todos(todos, params):
    if 'keyword' not in params.keys() and 'done' not in params.keys():
        return todos

    filtered_todos = list()
    done_filterd_todos = list()

    if 'done' in params.keys() and str(params['done']) in ['0', '1']:
        for todo in todos:
            if todo['done'] == params['done']:
                done_filterd_todos.append(todo)
    else:
        done_filterd_todos = todos

    if 'keyword' in params.keys() and params['keyword'] != '':
        target = 'both'
        if 'target' in params.keys() \
                and params['target'] in ['title', 'content']:
            target = params['target']

        for f_todo in done_filterd_todos:
            if target == 'title':
                search_string = f_todo['title']
            elif target == 'content':
                search_string = ''
                if 'content' in f_todo:
                    search_string = f_todo['content']
            else:
                search_string = f_todo['title']
                if 'content' in f_todo:
                    search_string += ' ' + f_todo['content']

            if search_string.find(params['keyword']) > 0:
                filtered_todos.append(f_todo)
    else:
        filtered_todos = done_filterd_todos

    return filtered_todos


def return_response(body, code):
    return Response(body=body,
                    status_code=code,
                    headers={'Content-Type': 'application/json'})
