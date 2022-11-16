from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404
from drf_problems.exceptions import exception_handler
from MySQLdb.constants.ER import DUP_ENTRY
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.serializers import ValidationError

from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


def wrapper(exc, context):
    if isinstance(exc, ObjectDoesNotExist):
        exc = HttpErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            detail="Object was not Found",
            title="Resource not found",
            extensions={"errors": exc.args},
        )
    elif isinstance(exc, Http404):
        exc = HttpErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
            title="Resource not found",
        )
    elif isinstance(exc, ValidationError):
        exc = HttpErrorResponse(
            status=status.HTTP_400_BAD_REQUEST,
            detail="Validation Error",
            title="Invalid input.",
            extensions={"errors": exc.detail},
        )
    elif isinstance(exc, ParseError):
        exc = HttpErrorResponse(
            status=status.HTTP_400_BAD_REQUEST,
            detail="Parsing JSON Error",
            title="Invalid input json.",
            extensions={"errors": exc.detail},
        )
    elif isinstance(exc, IntegrityError):
        if exc.args[0] == DUP_ENTRY:
            exc = HttpErrorResponse(
                status=status.HTTP_400_BAD_REQUEST,
                detail="This name already exists",
            )
        else:
            exc = HttpErrorResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return exception_handler(exc, context)
