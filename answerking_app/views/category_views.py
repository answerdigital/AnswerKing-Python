from django.db.models import QuerySet

from rest_framework import mixins, generics
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.utils.mixins.CategoryItemMixins import (
    CategoryItemUpdateMixin,
    CategoryItemRemoveMixin,
)
from answerking_app.models.models import Category

from answerking_app.models.serializers import (
    CategorySerializer,
)
from answerking_app.utils.mixins.GenericMixins import CreateMixin, UpdateMixin


class CategoryListView(
    mixins.ListModelMixin, CreateMixin, generics.GenericAPIView
):
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class CategoryDetailView(
    mixins.RetrieveModelMixin,
    UpdateMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)


class CategoryItemListView(
    CategoryItemUpdateMixin, CategoryItemRemoveMixin, generics.GenericAPIView
):
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    def put(
        self, request: Request, cat_id: int, item_id: int, *args, **kwargs
    ) -> Response:
        return self.update(request, cat_id, item_id, *args, **kwargs)

    def delete(
        self, request: Request, cat_id: int, item_id: int, *args, **kwargs
    ) -> Response:
        return self.remove(request, cat_id, item_id, *args, **kwargs)
