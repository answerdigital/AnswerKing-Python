from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


def NotFoundErrorDetailed():
    return HttpErrorResponse(
        status=404,
        detail="Not Found",
        title="Resource not found",
    )


class GetNotFoundDetailMixin(RetrieveModelMixin):
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().retrieve(request, *args, **kwargs)
        except (ObjectDoesNotExist, Http404):
            raise NotFoundErrorDetailed()


class UpdateNotFoundDetailMixin(RetrieveModelMixin):
    def update(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().update(request, *args, **kwargs)
        except (ObjectDoesNotExist, Http404):
            raise NotFoundErrorDetailed()
