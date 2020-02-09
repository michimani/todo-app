import app


class TestAppSubFunc:

    def test_generate_todo_id(self, monkeypatch):
        monkeypatch.setattr(
            'time.time',
            lambda: 1234567890.1234556
        )

        actual_todo_id = app.generate_todo_id()
        assert actual_todo_id == '1234567890123'

    def test_generate_todo_id_equal_13_digits(self, monkeypatch):
        monkeypatch.setattr(
            'time.time',
            lambda: 1234567890.012
        )

        actual_todo_id = app.generate_todo_id()
        assert actual_todo_id == '1234567890012'

    def test_generate_todo_id_less_13_digits(self, monkeypatch):
        monkeypatch.setattr(
            'time.time',
            lambda: 1234567890.0
        )

        actual_todo_id = app.generate_todo_id()
        assert actual_todo_id == '1234567890000'
