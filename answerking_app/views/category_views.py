from django.db.models import QuerySet
from rest_framework import generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Category
from answerking_app.models.serializers import CategorySerializer
from answerking_app.utils.mixins.CategoryProductMixins import (
    CategoryProductListMixin,
)
from answerking_app.utils.mixins.RetireMixin import RetireMixin
from answerking_app.utils.url_parameter_check import check_url_parameter


class CategoryListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class CategoryDetailView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    RetireMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        check_url_parameter(kwargs["pk"])
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs) -> Response:
        check_url_parameter(kwargs["pk"])
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        check_url_parameter(kwargs["pk"])
        return self.retire(request, *args, **kwargs)


class CategoryProductListView(
    CategoryProductListMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    def get(self, request: Request, cat_id, *args, **kwargs) -> Response:
        check_url_parameter(cat_id)
        return self.list(request, cat_id, *args, **kwargs)
