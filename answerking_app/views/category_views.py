from django.db.models import QuerySet
from rest_framework import generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Category
from answerking_app.models.serializers import CategorySerializer
from answerking_app.utils.mixins.CategoryProductMixins import (
    CategoryProductRemoveMixin,
    CategoryProductUpdateMixin,
)
from answerking_app.utils.mixins.IntegrityHandlerMixins import (
    CreateIntegrityHandlerMixin,
    UpdateIntegrityHandlerMixin,
)
from answerking_app.utils.mixins.NotFoundDetailMixins import (
    GetNotFoundDetailMixin,
    UpdateNotFoundDetailMixin,
)
from answerking_app.utils.mixins.RetireMixin import RetireMixin
from answerking_app.utils.mixins.SerializeErrorDetailRFCMixins import (
    CreateErrorDetailMixin,
    UpdateErrorDetailMixin,
)


class CategoryListView(
    mixins.ListModelMixin,
    CreateIntegrityHandlerMixin,
    CreateErrorDetailMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class CategoryDetailView(
    RetireMixin,
    GetNotFoundDetailMixin,
    UpdateNotFoundDetailMixin,
    UpdateIntegrityHandlerMixin,
    UpdateErrorDetailMixin,
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
        return self.retire(request, *args, **kwargs)


class CategoryProductListView(
    CategoryProductUpdateMixin,
    CategoryProductRemoveMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    def get(
        self, request: Request, cat_id: int, *args, **kwargs
    ) -> Response:
        return self.list(request, cat_id, *args, **kwargs)
