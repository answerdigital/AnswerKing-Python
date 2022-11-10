from MySQLdb.constants.ER import DUP_ENTRY
from django.db import IntegrityError
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response


class CreateMixin(CreateModelMixin):
    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as exc:
            return duplicate_check(exc)


class UpdateMixin(UpdateModelMixin):
    def update(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError as exc:
            return duplicate_check(exc)


class RetireMixin(UpdateModelMixin):
    def retire(self, request: Request, *args, **kwargs) -> Response:
        request.data["retired"] = True
        return super().partial_update(request, *args, **kwargs)


def duplicate_check(exc: IntegrityError) -> Response:
    if exc.args[0] == DUP_ENTRY:
        return Response(
            {"detail": "This name already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
