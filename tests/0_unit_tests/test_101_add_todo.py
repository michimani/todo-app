import app


class TestAddTodo:
    expected_todo = {
        'content': 'todo content',
        'done': '0',
        'l_idx_done': '0#999999',
        'title': 'Test todo',
        'todo_id': '999999',
        'user_id': '8cb2237d0679ca88db6464eac60da96345513964',
    }

    expected_put_todo_res = {
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
            'RetryAttempts': 0}}

    expected_invalid_params_error = ('key error: '
                                     'the following parameter '
                                     'is required: title')

    valid_request_body_dict = {
        'content': 'todo content',
        'title': 'Test todo',
    }

    invalid_request_body_dict_empty = {}

    invalid_request_body_dict_not_enough = {'content': ''}

    def test_add_todo(self, monkeypatch):
        self.set_monkeypatch_with_req_body(
            monkeypatch, self.valid_request_body_dict)

        actual_res = app.add_todo()
        assert actual_res.status_code == 200
        assert actual_res.body == self.expected_todo

    def test_add_todo_invalid_params_empty(self, monkeypatch):
        self.set_monkeypatch_with_req_body(
            monkeypatch, self.invalid_request_body_dict_empty)

        actual_res = app.add_todo()
        assert actual_res.status_code == 400
        assert actual_res.body == {
            'message': self.expected_invalid_params_error
        }

    def test_add_todo_invalid_params_not_enough(self, monkeypatch):
        self.set_monkeypatch_with_req_body(
            monkeypatch, self.invalid_request_body_dict_not_enough
        )

        actual_res = app.add_todo()
        assert actual_res.status_code == 400
        assert actual_res.body == {
            'message': self.expected_invalid_params_error
        }

    def set_monkeypatch_with_req_body(self, monkeypatch, req_body):
        monkeypatch.setattr(
            'chalicelib.db.put_todo',
            lambda t: self.expected_put_todo_res
        )
        monkeypatch.setattr(
            'app.generate_todo_id',
            lambda: '999999'
        )
        monkeypatch.setattr(
            'app.get_user_id',
            lambda: '8cb2237d0679ca88db6464eac60da96345513964'
        )
        monkeypatch.setattr(
            'app.get_bosy_as_dict',
            lambda: req_body
        )
