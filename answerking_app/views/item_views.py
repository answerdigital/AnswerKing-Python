from django.db.models import QuerySet
from rest_framework import generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Item
from answerking_app.models.serializers import ItemSerializer
from answerking_app.utils.mixins.ItemMixins import DestroyItemMixin
from answerking_app.utils.mixins.RetireMixin import RetireMixin


class ItemListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):

    queryset: QuerySet = Item.objects.all()
    serializer_class: ItemSerializer = ItemSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class ItemDetailView(
    mixins.RetrieveModelMixin,
    RetireMixin,
    DestroyItemMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Item.objects.all()
    serializer_class: ItemSerializer = ItemSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.retire(request, *args, **kwargs)
