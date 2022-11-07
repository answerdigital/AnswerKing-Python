from rest_framework import status
from rest_framework.exceptions import APIException


class Http400BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
