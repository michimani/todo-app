from chalice import Chalice
from chalicelib import db
from chalicelib import httpres
import time
import json
import hashlib

app = Chalice(app_name='todo-app')


@app.route('/todos', methods=['GET'], api_key_required=True)
def get_todos():
    user_id = get_user_id()
    query_params = get_query_params()

    if 'done' in query_params \
            and str(query_params['done']) in ['0', '1']:
        todos = db.get_todos_with_done(user_id, query_params['done'])
    else:
        todos = db.get_todos(user_id)

    filtered_todos = filter_todos(todos['Items'], query_params)
    return httpres.response_200(filtered_todos)


@app.route('/todos/{todo_id}', methods=['GET'], api_key_required=True)
def get_todo(todo_id):
    user_id = get_user_id()
    res = db.get_todo(user_id, todo_id)

    if 'Item' not in res:
        return httpres.response_404(todo_id)

    return httpres.response_200(res['Item'])


@app.route('/todos/{todo_id}', methods=['PATCH'], api_key_required=True)
def update_todo(todo_id):
    user_id = get_user_id()
    if db.todo_exists(user_id, todo_id) is False:
        return httpres.response_404(todo_id)

    params = get_bosy_as_dict()

    if 'title' not in params and 'content' not in params and 'done' not in params:
        return httpres.response_400(('parameter error: one of the following parameters is required: '
                                     'title, content, done'))

    if ('title' in params and params['title'] == '') \
            or ('done' in params and str(params['done']) not in ['0', '1']):
        return httpres.response_400(('parameter error: invalid value for one of the following parameters'
                                     ': title, done'))

    patch_data = {}
    if 'title' in params:
        patch_data['title'] = params['title']

    if 'content' in params:
        patch_data['content'] = params['content']

    if 'done' in params:
        patch_data['done'] = str(params['done'])
        patch_data['l_idx_done'] = '{}#{}'.format(str(params['done']), todo_id)

    try:
        res = db.update_todo(user_id, todo_id, patch_data)

        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            return httpres.response({
                'message': 'Failed to update a todo.'
            }, res['ResponseMetadata']['HTTPStatusCode'])

        return httpres.response_200(res['Attributes'])
    except Exception as e:
        return httpres.response_500(e)


@app.route('/todos/{todo_id}', methods=['DELETE'], api_key_required=True)
def delete_todo(todo_id):
    user_id = get_user_id()

    if db.todo_exists(user_id, todo_id) is False:
        return httpres.response_404(todo_id)

    try:
        res = db.delete_todo(user_id, todo_id)
        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            return httpres.response({
                'message': 'Failed to delete a todo.'
            }, res['ResponseMetadata']['HTTPStatusCode'])

        return httpres.response_200(res['Attributes'])
    except Exception as e:
        return httpres.response_500(e)


@app.route('/todos', methods=['POST'], api_key_required=True)
def add_todo():
    user_id = get_user_id()
    todo_id = generate_todo_id()
    req_body = get_bosy_as_dict()

    if 'title' not in req_body:
        return httpres.response_400('key error: the following parameter is required: title')

    new_todo = {
        'user_id': user_id,
        'todo_id': todo_id,
        'title': req_body['title'],
        'done': '0',
        'l_idx_done': '{}#{}'.format('0', todo_id)
    }

    if 'content' in req_body:
        new_todo['content'] = req_body['content']

    try:
        res = db.put_todo(new_todo)

        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            return httpres.response({
                'message': 'Failed to add a todo.'
            }, res['ResponseMetadata']['HTTPStatusCode'])

        return httpres.response_200(new_todo)
    except Exception as e:
        return httpres.response_500(e)


def generate_todo_id():
    return str(time.time()).replace('.', '')[:13].ljust(13, '0')


def get_user_id():
    return hashlib.sha1(app.current_request.headers['x-api-key'].encode('utf-8')).hexdigest()


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
    if 'keyword' not in params or params['keyword'] == '':
        return todos

    filtered_todos = list()

    target = 'both'
    if 'target' in params and params['target'] in ['title', 'content']:
        target = params['target']

    for todo in todos:
        if target == 'title':
            search_string = todo['title']
        elif target == 'content':
            search_string = ''
            if 'content' in todo:
                search_string = todo['content']
        else:
            search_string = todo['title']
            if 'content' in todo:
                search_string += ' ' + todo['content']

        if search_string.find(params['keyword']) >= 0:
            filtered_todos.append(todo)

    return filtered_todos
