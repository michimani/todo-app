import requests


class TestGetTodoApi:
    endpoint = 'http://localhost:8000/todos/'
    headers = {
        'content-type': 'application/json',
        'x-api-key': '123'
    }

    def test_get_todo(self):
        expected_todo = {
            'content': 'content of done todo',
            'done': '1',
            'l_idx_done': '1#1110000000001',
            'title': 'done todo with content',
            'todo_id': '1110000000001',
            'user_id': '40bd001563085fc35165329ea1ff5c5ecbdbbeef'
        }

        response = requests.get(
            self.endpoint + expected_todo['todo_id'],
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert response_json == expected_todo

    def test_get_todo_not_found_error(self):
        response = requests.get(
            self.endpoint + '999',
            headers=self.headers
        )

        assert response.status_code == 404

        response_json = response.json()

        assert response_json['message'] == 'not found error: todo with Id = 999 was not found'
