import requests


class TestGetTodosApi:
    endpoint = 'http://localhost:8000/todos/'
    headers = {
        'content-type': 'application/json',
        'x-api-key': '123'
    }

    def test_get_todos(self):
        response = requests.get(
            self.endpoint,
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert len(response_json) == 9

    def test_get_todos_with_done(self):
        params = {'done': '1'}
        response = requests.get(
            self.endpoint,
            params=params,
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        for todo in response_json:
            assert todo['done'] == '1'

    def test_get_todos_with_invalid_done(self):
        params = {'done': '9'}
        response = requests.get(
            self.endpoint,
            params=params,
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        for todo in response_json:
            assert todo['done'] == '1' or todo['done'] == '0'

    def test_get_todos_with_keyword_both(self):
        params = {'keyword': 'todo'}
        response = requests.get(
            self.endpoint,
            params=params,
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        for todo in response_json:
            check_string = todo['title']
            if 'content' in todo:
                check_string += ' ' + todo['content']
            assert check_string.find(params['keyword']) >= 0

    def test_get_todos_with_keyword_title(self):
        params = {'keyword': 'todo', 'target': 'title'}
        response = requests.get(
            self.endpoint,
            params=params,
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        for todo in response_json:
            assert todo['title'].find(params['keyword']) >= 0

    def test_get_todos_with_keyword_content(self):
        params = {'keyword': 'todo', 'target': 'content'}
        response = requests.get(
            self.endpoint,
            params=params,
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        for todo in response_json:
            assert todo['content'].find(params['keyword']) >= 0

    def test_get_todos_with_keyword_japanese(self):
        params = {'keyword': '詳細'}
        response = requests.get(
            self.endpoint,
            params=params,
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        for todo in response_json:
            check_string = todo['title']
            if 'content' in todo:
                check_string += ' ' + todo['content']
            assert check_string.find(params['keyword']) >= 0

    def test_get_todos_not_match(self):
        params = {'keyword': '存在しないToDo'}
        response = requests.get(
            self.endpoint,
            params=params,
            headers=self.headers
        )

        assert response.status_code == 200

        response_json = response.json()

        assert len(response_json) == 0
