import app


class TestGetTodo:
    expected_todo = {
        'Id': '999999',
        'Titile': 'Test todo',
        'Done': 0
    }

    expected_todo_not_found = {
        'message': 'not found error: todo with Id = 123 was not found'
    }

    def test_get_todo(self, monkeypatch):
        monkeypatch.setattr(
            'chalicelib.db.get_todo',
            lambda _: {'Item': self.expected_todo}
        )

        actual_todo = app.get_todo('999999')
        assert actual_todo.status_code == 200
        assert actual_todo.body == self.expected_todo

    def test_get_todo_not_found(self, monkeypatch):
        monkeypatch.setattr(
            'chalicelib.db.get_todo',
            lambda _: {}
        )

        actual_todo = app.get_todo('123')
        assert actual_todo.status_code == 404
        assert actual_todo.body == self.expected_todo_not_found
