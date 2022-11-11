from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Product
from answerking_app.models.serializers import CategorySerializer
from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


class CategoryProductUpdateMixin:
    def update(
        self, request: Request, cat_id: int, product_id: int, *args, **kwargs
    ) -> Response:

        category: Category = get_object_or_404(Category, pk=cat_id)
        product: Product = get_object_or_404(Product, pk=product_id)

        if product in category.products.all():
            raise HttpErrorResponse(
                status=status.HTTP_400_BAD_REQUEST,
                detail="Product is already in the category",
            )

        category.products.add(product)
        response: ReturnDict = CategorySerializer(category).data
        return Response(response, status=status.HTTP_200_OK)


class CategoryProductRemoveMixin:
    def remove(
        self, request: Request, cat_id: int, product_id: int, *args, **kwargs
    ) -> Response:
        category: Category = get_object_or_404(Category, pk=cat_id)
        product: Product = get_object_or_404(category.products, id=product_id)
        category.products.remove(product)
        response: ReturnDict = CategorySerializer(category).data
        return Response(response, status=status.HTTP_200_OK)
