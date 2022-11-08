from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Item
from answerking_app.models.serializers import CategorySerializer
from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


class CategoryItemUpdateMixin:
    def update(
        self, request: Request, cat_id: int, item_id: int, *args, **kwargs
    ) -> Response:

        category: Category = get_object_or_404(Category, pk=cat_id)
        item: Item = get_object_or_404(Item, pk=item_id)

        if item in category.items.all():
            raise HttpErrorResponse(status=status.HTTP_400_BAD_REQUEST)

        category.items.add(item)
        response: ReturnDict = CategorySerializer(category).data
        return Response(response, status=status.HTTP_200_OK)


class CategoryItemRemoveMixin:
    def remove(
        self, request: Request, cat_id: int, item_id: int, *args, **kwargs
    ) -> Response:
        category: Category = get_object_or_404(Category, pk=cat_id)
        item: Item = get_object_or_404(category.items, id=item_id)
        category.items.remove(item)
        response: ReturnDict = CategorySerializer(category).data
        return Response(response, status=status.HTTP_200_OK)
