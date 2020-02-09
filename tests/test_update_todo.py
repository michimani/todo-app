import app


class TestUpdateTodo:
    expected_todo = {
        'content': 'todo content',
        'done': '1',
        'l_idx_done': '1#999999',
        'title': 'Test todo',
        'todo_id': '999999',
        'user_id': '8cb2237d0679ca88db6464eac60da96345513964',
    }

    expected_update_todo_res = {
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

    expected_not_enough_params_error = ('parameter error: one of the following parameters '
                                        'is required: title, content, done')

    expected_invalid_value_params_error = ('parameter error: invalid value for one of '
                                           'the following parameters: title, done')

    valid_request_body_dict = {
        'content': 'todo content',
        'done': '1',
        'title': 'Test todo',
    }

    invalid_request_body_dict_empty = {}

    invalid_request_body_dict_invaid_value_title = {'title': ''}

    invalid_request_body_dict_invaid_value_done = {'done': '4'}

    def test_update_todo(self, monkeypatch):
        self.set_monkeypatch_with_req_body(
            monkeypatch, self.valid_request_body_dict)

        actual_res = app.update_todo('999999')
        assert actual_res.status_code == 200
        assert actual_res.body == self.expected_todo

    def test_update_todo_not_found(self, monkeypatch):
        self.set_monkeypatch_with_req_body(
            monkeypatch, self.valid_request_body_dict, exists=False)

        actual_res = app.update_todo('123')
        assert actual_res.status_code == 404
        assert actual_res.body == {
            'message': self.expected_not_found_error
        }

    def test_update_todo_invalid_params_empty(self, monkeypatch):
        self.set_monkeypatch_with_req_body(
            monkeypatch, self.invalid_request_body_dict_empty)

        actual_res = app.update_todo('999999')
        assert actual_res.status_code == 400
        assert actual_res.body == {
            'message': self.expected_not_enough_params_error
        }

    def test_update_todo_invalid_value_title(self, monkeypatch):
        self.set_monkeypatch_with_req_body(
            monkeypatch, self.invalid_request_body_dict_invaid_value_title
        )

        actual_res = app.update_todo('999999')
        assert actual_res.status_code == 400
        assert actual_res.body == {
            'message': self.expected_invalid_value_params_error
        }

    def test_update_todo_invalid_value_done(self, monkeypatch):
        self.set_monkeypatch_with_req_body(
            monkeypatch, self.invalid_request_body_dict_invaid_value_done
        )

        actual_res = app.update_todo('999999')
        assert actual_res.status_code == 400
        assert actual_res.body == {
            'message': self.expected_invalid_value_params_error
        }

    def set_monkeypatch_with_req_body(self, monkeypatch, req_body, exists=True):
        monkeypatch.setattr(
            'chalicelib.db.update_todo',
            lambda u, t, p: self.expected_update_todo_res
        )
        monkeypatch.setattr(
            'chalicelib.db.todo_exists',
            lambda u, t: exists
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
