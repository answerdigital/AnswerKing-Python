from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


def NotFoundErrorDetailed(exc: Http404 | ObjectDoesNotExist):
    if isinstance(exc, ObjectDoesNotExist):
        return HttpErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            detail="Object was not Found",
            title="Resource not found",
            extensions={"errors": exc.args},
        )
    elif isinstance(exc, Http404):
        return HttpErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
            title="Resource not found",
        )
    else:
        return HttpErrorResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetNotFoundDetailMixin(RetrieveModelMixin):
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().retrieve(request, *args, **kwargs)
        except (ObjectDoesNotExist, Http404) as exc:
            raise NotFoundErrorDetailed(exc)


class UpdateNotFoundDetailMixin(UpdateModelMixin):
    def update(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().update(request, *args, **kwargs)
        except (ObjectDoesNotExist, Http404) as exc:
            raise NotFoundErrorDetailed(exc)
