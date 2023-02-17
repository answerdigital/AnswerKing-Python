import re

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from answerking_app.models.models import Product
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails


def compress_white_spaces(value: str) -> str:
    return re.sub(" +", " ", value.strip())


def products_check(validated_data: dict) -> list[Product]:
    products: list[Product] = validated_data.get("product_set", [])
    for product in products:
        try:
            if product.retired:
                raise ProblemDetails(
                    status=status.HTTP_410_GONE,
                    detail="This product has been retired",
                )
        except (ObjectDoesNotExist, AttributeError) as exc:
            raise ProblemDetails(
                status=status.HTTP_400_BAD_REQUEST,
                detail="Product was not Found",
                title="Product not found",
                extensions={"errors": exc.args},
            )
    return products
