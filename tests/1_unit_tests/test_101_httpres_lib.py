from chalicelib import httpres


class TestHttpresLib:
    def test_response_200(self, monkeypatch):
        expected_body = {
            'message': 'Expected body'
        }

        actual_res = httpres.response_200(expected_body)
        assert actual_res.body == expected_body
        assert actual_res.status_code == 200

    def test_response_400(self, monkeypatch):
        expected_message = '400 error message'

        actual_res = httpres.response_400(expected_message)
        assert actual_res.body == {'message': expected_message}
        assert actual_res.status_code == 400

    def test_response_404(self, monkeypatch):
        expected_message = 'not found error: todo with Id = 123 was not found'

        actual_res_num = httpres.response_404(123)
        assert actual_res_num.body == {'message': expected_message}
        assert actual_res_num.status_code == 404

        actual_res_str = httpres.response_404('123')
        assert actual_res_str.body == {'message': expected_message}
        assert actual_res_str.status_code == 404

    def test_response_500(self, monkeypatch):
        expected_message = 'manual Exception message'

        try:
            raise Exception('manual Exception message')
        except Exception as e:
            actual_res = httpres.response_500(e)

        assert actual_res.body == {'message': expected_message}
        assert actual_res.status_code == 500
