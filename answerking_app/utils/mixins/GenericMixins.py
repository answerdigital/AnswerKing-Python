from typing import NoReturn

from django.db import IntegrityError
from MySQLdb.constants.ER import DUP_ENTRY
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.utils.mixins.ApiExceptions import Http400BadRequest


class CreateMixin(CreateModelMixin):
    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as exc:
            handle_IntegrityError(exc)


class UpdateMixin(UpdateModelMixin):
    def update(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError as exc:
            return handle_IntegrityError(exc)


class RetireMixin(UpdateModelMixin):
    def retire(self, request: Request, *args, **kwargs) -> Response:
        request.data["retired"] = True
        return super().partial_update(request, *args, **kwargs)


def handle_IntegrityError(exc: IntegrityError) -> NoReturn:
    if exc.args[0] == DUP_ENTRY:
        raise Http400BadRequest
    else:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
