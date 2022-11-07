from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Item
from answerking_app.models.serializers import CategorySerializer
from answerking_app.utils.ErrorType import ErrorMessage

from django.shortcuts import get_object_or_404

from answerking_app.utils.mixins.GenericMixins import duplicate_check


class CategoryItemUpdateMixin:
    def duplicate_item_check(self, category: Category, item: Item, *args, **kwargs):

        if item in category.items.all():
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Item already in category",
                }
            }
            raise ValueError(error_msg)

    def update_single_item(self, request: Request, cat_id: int, item_id: int, *args, **kwargs):
        try:
            category: Category = get_object_or_404(Category, pk=cat_id)
            item: Item = get_object_or_404(Item, pk=item_id)
            self.duplicate_item_check(category=category, item=item)
            category.items.add(item)

            response: ReturnDict = CategorySerializer(category).data
            return Response(response, status=status.HTTP_200_OK)
        except ValueError as err:
            return Response(
                err.args,
                status=status.HTTP_400_BAD_REQUEST,
            )


class CategoryUpdateMixin(CategoryItemUpdateMixin):
    def update_items(self, category: Category, items: list):
        for item in items:
            item: Item = get_object_or_404(Item, pk=item['id'])
            self.duplicate_item_check(category=category, item=item)
            category.items.add(item)

    def update_name(self, category: Category, new_name: str):
        category.name = new_name
        category.save()

    def category_check_and_update(self, request: Request, pk: int, *args, **kwargs):
        try:
            category: Category = get_object_or_404(Category, pk=pk)
            serialized_body: CategorySerializer = CategorySerializer(
                data=request.data
            )
            serialized_body.is_valid(raise_exception=True)

            if 'name' in serialized_body.data:
                self.update_name(category, new_name=serialized_body.data['name'])
            if 'items' in serialized_body.data:
                self.update_items(category, items=serialized_body.data['items'])

            response: ReturnDict = CategorySerializer(category).data
            return Response(response, status=status.HTTP_200_OK)
        except IntegrityError as exc:
            return duplicate_check(exc)
        except ValueError as err:
            return Response(
                err.args,
                status=status.HTTP_400_BAD_REQUEST,
            )


class CategoryItemRemoveMixin:
    def remove(
        self, request: Request, cat_id: int, item_id: int, *args, **kwargs
    ) -> Response:
        category: Category = get_object_or_404(Category, pk=cat_id)
        item: Item = get_object_or_404(category.items, id=item_id)
        category.items.remove(item)
        response: ReturnDict = CategorySerializer(category).data
        return Response(response, status=status.HTTP_200_OK)
