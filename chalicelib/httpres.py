from chalice import Response
import sys


def response_200(body):
    return response(body, 200)


def response_400(message):
    return response({
        'message': message,
    }, 400)


def response_404(todo_id):
    return response({
        'message': ('not found error: todo with '
                    'Id = {todo_id} was not found').format(todo_id=todo_id)
    }, 404)


def response_500(exception):
    traceback = sys.exc_info()[2]
    return response({
        'message': str(exception.with_traceback(traceback)),
    }, 500)


def response(body, code):
    return Response(body=body,
                    status_code=code,
                    headers={'Content-Type': 'application/json'})
