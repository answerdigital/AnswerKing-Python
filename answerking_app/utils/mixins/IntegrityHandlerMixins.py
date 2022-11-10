from typing import NoReturn

from django.db import IntegrityError
from MySQLdb.constants.ER import DUP_ENTRY
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


class CreateIntegrityHandlerMixin(CreateModelMixin):
    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as exc:
            handle_IntegrityError(exc)


class UpdateIntegrityHandlerMixin(UpdateModelMixin):
    def update(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError as exc:
            return handle_IntegrityError(exc)


def handle_IntegrityError(exc: IntegrityError) -> NoReturn:
    if exc.args[0] == DUP_ENTRY:
        raise HttpErrorResponse(
            status=status.HTTP_400_BAD_REQUEST,
            detail="This name already exists",
        )
    else:
        raise HttpErrorResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
