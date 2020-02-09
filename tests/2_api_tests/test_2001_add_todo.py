import json
import requests


class TestAddTodoApi:
    endpoint = 'http://localhost:8000/todos/'
    headers = {
        'content-type': 'application/json',
        'x-api-key': '123'
    }

    def test_add_todo(self):
        expected_todo = {
            'title': 'new todo',
            'content': 'content of new todo'
        }
        expected_user_id = '40bd001563085fc35165329ea1ff5c5ecbdbbeef'

        response = requests.post(
            self.endpoint,
            data=json.dumps(expected_todo),
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json['todo_id']
        assert response_json['l_idx_done'] == '0#' + response_json['todo_id']
        assert response_json['user_id'] == expected_user_id
        assert response_json['done'] == '0'
        assert response_json['title'] == expected_todo['title']
        assert response_json['content'] == expected_todo['content']

    def test_add_todo_only_title(self):
        expected_todo = {
            'title': 'new todo only title',
        }
        expected_user_id = '40bd001563085fc35165329ea1ff5c5ecbdbbeef'

        response = requests.post(
            self.endpoint,
            data=json.dumps(expected_todo),
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json['todo_id']
        assert response_json['l_idx_done'] == '0#' + response_json['todo_id']
        assert response_json['user_id'] == expected_user_id
        assert response_json['done'] == '0'
        assert response_json['title'] == expected_todo['title']
        assert 'content' not in response_json

    def test_add_todo_japanese(self):
        expected_todo = {
            'title': '新しい ToDo',
            'content': '新しい ToDo の詳細'
        }
        expected_user_id = '40bd001563085fc35165329ea1ff5c5ecbdbbeef'

        response = requests.post(
            self.endpoint,
            data=json.dumps(expected_todo),
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json['todo_id']
        assert response_json['l_idx_done'] == '0#' + response_json['todo_id']
        assert response_json['user_id'] == expected_user_id
        assert response_json['done'] == '0'
        assert response_json['title'] == expected_todo['title']
        assert response_json['content'] == expected_todo['content']

    def test_add_todo_error_key(self):
        response = requests.post(
            self.endpoint,
            data=json.dumps({}),
            headers=self.headers
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json['message'] == 'key error: the following parameter is required: title'

    def test_add_todo_error_empty_value(self):
        response = requests.post(
            self.endpoint,
            data=json.dumps({'title': ''}),
            headers=self.headers
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json['message'] == 'key error: the following parameter is required: title'
