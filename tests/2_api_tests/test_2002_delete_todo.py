import requests


class TestDeleteTodoApi:
    endpoint = 'http://localhost:8000/todos/'
    headers = {
        'content-type': 'application/json',
        'x-api-key': '123'
    }

    def test_delete_todo(self):
        expected_todo = {
            'content': 'content of todo 2',
            'done': '0',
            'l_idx_done': '0#1010000000002',
            'title': 'todo with content 2',
            'todo_id': '1010000000002',
            'user_id': '40bd001563085fc35165329ea1ff5c5ecbdbbeef'
        }

        response = requests.delete(
            self.endpoint + expected_todo['todo_id'],
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json == expected_todo

    def test_delete_todo_not_found_error(self):
        response = requests.delete(
            self.endpoint + '999',
            headers=self.headers
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json['message'] == 'not found error: todo with Id = 999 was not found'
