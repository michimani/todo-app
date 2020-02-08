import app


class TestGetTodo:
    expected_todo = {
        'content': 'todo content',
        'done': '0',
        'l_idx_done': '0#999999',
        'title': 'Test todo',
        'todo_id': '999999',
        'user_id': '8cb2237d0679ca88db6464eac60da96345513964',
    }

    expected_todo_not_found = {
        'message': 'not found error: todo with Id = 123 was not found'
    }

    def test_get_todo(self, monkeypatch):
        monkeypatch.setattr(
            'chalicelib.db.get_todo',
            lambda u, t: {'Item': self.expected_todo}
        )
        monkeypatch.setattr(
            'app.get_user_id',
            lambda: '8cb2237d0679ca88db6464eac60da96345513964'
        )

        actual_todo = app.get_todo('999999')
        assert actual_todo.status_code == 200
        assert actual_todo.body == self.expected_todo

    def test_get_todo_not_found(self, monkeypatch):
        monkeypatch.setattr(
            'chalicelib.db.get_todo',
            lambda u, t: {}
        )
        monkeypatch.setattr(
            'app.get_user_id',
            lambda: '8cb2237d0679ca88db6464eac60da96345513964'
        )

        actual_todo = app.get_todo('123')
        assert actual_todo.status_code == 404
        assert actual_todo.body == self.expected_todo_not_found
