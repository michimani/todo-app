import app


class TestDeleteTodo:
    expected_todo = {
        'content': 'todo content',
        'done': '0',
        'l_idx_done': '0#999999',
        'title': 'Test todo',
        'todo_id': '999999',
        'user_id': '8cb2237d0679ca88db6464eac60da96345513964',
    }

    expected_delete_todo_res = {
        'ResponseMetadata': {
            'RequestId': '2feb102a-3157-49f8-a988-bdfeff6739ea',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'content-type': 'application/x-amz-json-1.0',
                'x-amz-crc32': '2745614147',
                'x-amzn-requestid': '2feb102a-3157-49f8-a988-bdfeff6739ea',
                'content-length': '2',
                'server': 'Jetty(8.1.12.v20130726)'
            },
            'RetryAttempts': 0},
        'Attributes': expected_todo}

    expected_not_found_error = 'not found error: todo with Id = 123 was not found'

    def test_delete_todo(self, monkeypatch):
        self.set_monkeypatch_attrs(monkeypatch, exists=True)

        actual_res = app.delete_todo('999999')
        assert actual_res.status_code == 200
        assert actual_res.body == self.expected_todo

    def test_delete_todo_not_found(self, monkeypatch):
        self.set_monkeypatch_attrs(monkeypatch, exists=False)

        actual_res = app.delete_todo('123')
        assert actual_res.status_code == 404
        assert actual_res.body == {
            'message': self.expected_not_found_error
        }

    def set_monkeypatch_attrs(self, monkeypatch, exists=True):
        monkeypatch.setattr(
            'app.get_user_id',
            lambda: '8cb2237d0679ca88db6464eac60da96345513964'
        )
        monkeypatch.setattr(
            'chalicelib.db.todo_exists',
            lambda u, t: exists
        )
        monkeypatch.setattr(
            'chalicelib.db.delete_todo',
            lambda u, t: self.expected_delete_todo_res
        )
