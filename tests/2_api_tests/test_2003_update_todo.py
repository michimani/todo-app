import json
import requests


class TestUpdateTodoApi:
    endpoint = 'http://localhost:8000/todos/'
    headers = {
        'content-type': 'application/json',
        'x-api-key': '123'
    }

    def test_update_todo_done(self):
        expected_todo = {
            'content': 'content of todo 1',
            'done': '1',
            'l_idx_done': '1#1010000000001',
            'title': 'todo with content 1',
            'todo_id': '1010000000001',
            'user_id': '40bd001563085fc35165329ea1ff5c5ecbdbbeef'
        }

        response = requests.patch(
            self.endpoint + expected_todo['todo_id'],
            data=json.dumps({'done': '1'}),
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json == expected_todo

    def test_update_todo_title(self):
        expected_todo = {
            'content': 'content of todo 1',
            'done': '1',
            'l_idx_done': '1#1010000000001',
            'title': 'todo with content 1 updated',
            'todo_id': '1010000000001',
            'user_id': '40bd001563085fc35165329ea1ff5c5ecbdbbeef'
        }

        response = requests.patch(
            self.endpoint + expected_todo['todo_id'],
            data=json.dumps({'title': 'todo with content 1 updated'}),
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json == expected_todo

    def test_update_todo_content(self):
        expected_todo = {
            'content': 'content of todo 1 updated',
            'done': '1',
            'l_idx_done': '1#1010000000001',
            'title': 'todo with content 1 updated',
            'todo_id': '1010000000001',
            'user_id': '40bd001563085fc35165329ea1ff5c5ecbdbbeef'
        }

        response = requests.patch(
            self.endpoint + expected_todo['todo_id'],
            data=json.dumps({'content': 'content of todo 1 updated'}),
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json == expected_todo

    def test_update_todo_empty_content(self):
        expected_todo = {
            'done': '1',
            'l_idx_done': '1#1010000000001',
            'title': 'todo with content 1 updated',
            'todo_id': '1010000000001',
            'user_id': '40bd001563085fc35165329ea1ff5c5ecbdbbeef'
        }

        response = requests.patch(
            self.endpoint + expected_todo['todo_id'],
            data=json.dumps({'content': ''}),
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json == expected_todo

    def test_update_todo_all(self):
        expected_todo = {
            'content': 'content of todo 1',
            'done': '0',
            'l_idx_done': '0#1010000000001',
            'title': 'todo with content 1',
            'todo_id': '1010000000001',
            'user_id': '40bd001563085fc35165329ea1ff5c5ecbdbbeef'
        }

        response = requests.patch(
            self.endpoint + expected_todo['todo_id'],
            data=json.dumps({
                'done': '0',
                'title': 'todo with content 1',
                'content': 'content of todo 1'}),
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json == expected_todo

    def test_update_todo_japanese(self):
        expected_todo = {
            'content': 'ToDo 1 の詳細',
            'done': '0',
            'l_idx_done': '0#1010000000001',
            'title': '詳細を含む ToDo 1',
            'todo_id': '1010000000001',
            'user_id': '40bd001563085fc35165329ea1ff5c5ecbdbbeef'
        }

        response = requests.patch(
            self.endpoint + expected_todo['todo_id'],
            data=json.dumps({
                'title': '詳細を含む ToDo 1',
                'content': 'ToDo 1 の詳細'}),
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json == expected_todo

    def test_update_todo_no_key_error(self):
        response = requests.patch(
            self.endpoint + '1010000000001',
            headers=self.headers
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json['message'] == ('parameter error: one of the following parameters is '
                                            'required: title, content, done')

    def test_update_todo_invalid_title_error(self):
        response = requests.patch(
            self.endpoint + '1010000000001',
            data=json.dumps({'title': ''}),
            headers=self.headers
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json['message'] == ('parameter error: invalid value for one of '
                                            'the following parameters: title, done')

    def test_update_todo_invalid_done_error(self):
        response = requests.patch(
            self.endpoint + '1010000000001',
            data=json.dumps({'done': '9'}),
            headers=self.headers
        )

        assert response.status_code == 400

        response_json = response.json()

        assert response_json['message'] == ('parameter error: invalid value for one of '
                                            'the following parameters: title, done')

    def test_update_todo_not_found_error(self):
        response = requests.patch(
            self.endpoint + '999',
            headers=self.headers
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json['message'] == 'not found error: todo with Id = 999 was not found'
