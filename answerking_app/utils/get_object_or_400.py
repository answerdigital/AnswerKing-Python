from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


def get_object_or_400(object_class, pk, *filter_args, **filter_kwargs):
    try:
        requested_object = object_class.objects.get(pk=pk)
    except ObjectDoesNotExist as exc:
        raise HttpErrorResponse(
            status=status.HTTP_400_BAD_REQUEST,
            detail="Product was not Found",
            title="Product not found.",
            extensions={"errors": exc.args},
        )
    return requested_object
