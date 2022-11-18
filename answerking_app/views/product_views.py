from django.db.models import QuerySet
from rest_framework import generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Product
from answerking_app.models.serializers import ProductSerializer
from answerking_app.utils.mixins.RetireMixin import RetireMixin


class ProductListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):

    queryset: QuerySet = Product.objects.all()
    serializer_class: ProductSerializer = ProductSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class ProductDetailView(
    mixins.RetrieveModelMixin,
    RetireMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Product.objects.all()
    serializer_class: ProductSerializer = ProductSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.retire(request, *args, **kwargs)
