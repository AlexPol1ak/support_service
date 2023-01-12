from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Расширяет возвращаемые исключения в json. """

    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code

    return response