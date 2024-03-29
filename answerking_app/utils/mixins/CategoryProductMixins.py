from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Product, Category
from answerking_app.models.serializers import ProductSerializer
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails


class CategoryProductListMixin:
    def list(self, **kwargs) -> Response:
        try:
            Category.objects.get(pk=kwargs["pk"])
        except ObjectDoesNotExist:
            raise ProblemDetails(
                status=status.HTTP_404_NOT_FOUND,
                detail="Not Found",
                title="Resource not found",
            )

        products: QuerySet[Product] = Product.objects.filter(
            category__id=kwargs["pk"]
        )
        if not products:
            raise ProblemDetails(status=status.HTTP_404_NOT_FOUND)
        response = ProductSerializer(products, many=True).data

        return Response(response, status=status.HTTP_200_OK)
