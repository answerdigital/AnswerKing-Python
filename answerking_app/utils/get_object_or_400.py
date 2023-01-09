from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from answerking_app.utils.mixins.ApiExceptions import ProblemDetails


def get_product_or_400(object_class, pk):
    try:
        requested_object = object_class.objects.get(pk=pk)
    except ObjectDoesNotExist as exc:
        raise ProblemDetails(
            status=status.HTTP_400_BAD_REQUEST,
            detail="Product was not found",
            title="Product not found",
            extensions={"errors": exc.args},
        )
    return requested_object
