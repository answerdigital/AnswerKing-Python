from rest_framework.exceptions import ParseError
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


def ValidationErrorDetailed(exc: ValidationError | ParseError):
    if isinstance(exc, ValidationError):
        return HttpErrorResponse(
            status=400,
            detail="Validation Error",
            title="Invalid input.",
            extensions={"errors": exc.detail},
        )
    elif isinstance(exc, ParseError):
        return HttpErrorResponse(
            status=400,
            detail="Parsing JSON Error",
            title="Invalid input json.",
            extensions={"errors": exc.detail},
        )


class CreateErrorDetailMixin(CreateModelMixin):
    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().create(request, *args, **kwargs)
        except (ValidationError, ParseError) as exc:
            raise ValidationErrorDetailed(exc)


class UpdateErrorDetailMixin(UpdateModelMixin):
    def update(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().update(request, *args, **kwargs)
        except (ValidationError, ParseError) as exc:
            raise ValidationErrorDetailed(exc)
