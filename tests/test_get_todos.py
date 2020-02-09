import app


class TestGetTodos:
    not_done_todos = [
        {
            'content': 'todo content 1',
            'done': '0',
            'l_idx_done': '0#9999991',
            'title': 'テスト todo 1',
            'todo_id': '9999991',
            'user_id': '8cb2237d0679ca88db6464eac60da96345513964',
        },
        {
            'content': '詳細 2',
            'done': '0',
            'l_idx_done': '0#9999992',
            'title': 'Test todo 2',
            'todo_id': '9999992',
            'user_id': '8cb2237d0679ca88db6464eac60da96345513964',
        },
        {
            'content': 'とぅーどぅー 3',
            'done': '0',
            'l_idx_done': '0#9999993',
            'title': 'Test todo 3',
            'todo_id': '9999993',
            'user_id': '8cb2237d0679ca88db6464eac60da96345513964',
        }
    ]

    done_todos = [
        {
            'content': 'todo content 4',
            'done': '1',
            'l_idx_done': '1#9999994',
            'title': 'テスト todo 4',
            'todo_id': '9999994',
            'user_id': '8cb2237d0679ca88db6464eac60da96345513964',
        },
        {
            'content': '詳細 5',
            'done': '1',
            'l_idx_done': '1#9999995',
            'title': 'Test todo 5',
            'todo_id': '9999995',
            'user_id': '8cb2237d0679ca88db6464eac60da96345513964',
        },
        {
            'content': 'とぅーどぅー 6',
            'done': '1',
            'l_idx_done': '1#9999996',
            'title': 'Test todo 6',
            'todo_id': '9999996',
            'user_id': '8cb2237d0679ca88db6464eac60da96345513964',
        }
    ]

    def test_get_todos(self, monkeypatch):
        self.set_monkeypatch_with_req_query(
            monkeypatch, {})

        actual_res = app.get_todos()
        assert actual_res.status_code == 200
        assert actual_res.body == self.done_todos + self.not_done_todos

    def test_get_todos_done(self, monkeypatch):
        self.set_monkeypatch_with_req_query(
            monkeypatch, {'done': '1'}, '1')

        actual_res = app.get_todos()
        assert actual_res.status_code == 200
        assert actual_res.body == self.done_todos

    def test_get_todos_not_done(self, monkeypatch):
        self.set_monkeypatch_with_req_query(
            monkeypatch, {'done': '0'}, '0')

        actual_res = app.get_todos()
        assert actual_res.status_code == 200
        assert actual_res.body == self.not_done_todos

    def test_get_todos_keyword_both(self, monkeypatch):
        self.set_monkeypatch_with_req_query(
            monkeypatch, {'keyword': 'todo'}
        )

        expected_todos = self.done_todos + self.not_done_todos

        actual_res = app.get_todos()
        assert actual_res.status_code == 200
        assert actual_res.body == expected_todos

    def test_get_todos_keyword_title(self, monkeypatch):
        self.set_monkeypatch_with_req_query(
            monkeypatch, {'keyword': 'テスト', 'target': 'title'}
        )

        expected_todos = [
            self.done_todos[0],
            self.not_done_todos[0],
        ]

        actual_res = app.get_todos()
        assert actual_res.status_code == 200
        assert actual_res.body == expected_todos

    def test_get_todos_keyword_content(self, monkeypatch):
        self.set_monkeypatch_with_req_query(
            monkeypatch, {'keyword': 'とぅ', 'target': 'content'}
        )

        expected_todos = [
            self.done_todos[2],
            self.not_done_todos[2],
        ]

        actual_res = app.get_todos()
        assert actual_res.status_code == 200
        assert actual_res.body == expected_todos

    def test_get_todos_keyword_not_match_both(self, monkeypatch):
        self.set_monkeypatch_with_req_query(
            monkeypatch, {'keyword': 'abcdefg'}
        )

        actual_res = app.get_todos()
        assert actual_res.status_code == 200
        assert actual_res.body == []

    def test_get_todos_keyword_not_match_title(self, monkeypatch):
        self.set_monkeypatch_with_req_query(
            monkeypatch, {'keyword': 'テスト', 'target': 'content'}
        )

        actual_res = app.get_todos()
        assert actual_res.status_code == 200
        assert actual_res.body == []

    def test_get_todos_keyword_not_match_content(self, monkeypatch):
        self.set_monkeypatch_with_req_query(
            monkeypatch, {'keyword': 'とぅ', 'target': 'title'}
        )

        actual_res = app.get_todos()
        assert actual_res.status_code == 200
        assert actual_res.body == []

    def test_get_todos_invalid_params(self, monkeypatch):
        self.set_monkeypatch_with_req_query(
            monkeypatch, {'somekey': 'とぅ', 'done': 'invlid value'}
        )

        expected_todos = self.done_todos + self.not_done_todos

        actual_res = app.get_todos()
        assert actual_res.status_code == 200
        assert actual_res.body == expected_todos

    def set_monkeypatch_with_req_query(self, monkeypatch, req_query, done='0'):
        monkeypatch.setattr(
            'chalicelib.db.get_todos',
            lambda u: {'Items': self.done_todos + self.not_done_todos}
        )
        monkeypatch.setattr(
            'chalicelib.db.get_todos_with_done',
            lambda u, d: {'Items': self.done_todos if done ==
                          '1' else self.not_done_todos}
        )
        monkeypatch.setattr(
            'app.get_user_id',
            lambda: '8cb2237d0679ca88db6464eac60da96345513964'
        )
        monkeypatch.setattr(
            'app.get_query_params',
            lambda: req_query
        )
