from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from django.http import Http404
from django.core.exceptions import PermissionDenied


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, APIException):
            code = exc.get_codes()
        elif isinstance(exc, Http404):
            code = 'not_found'
        elif isinstance(exc, PermissionDenied):
            code = 'permission_denied'
        else:
            raise AttributeError

        response.data = {
            'code': code,
            'status': response.status_code,
            'error': response.data
        }

    return response