from django.db.models import QuerySet
from rest_framework import mixins, generics
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.utils.mixins.GenericMixins import CreateMixin, UpdateMixin
from answerking_app.utils.mixins.ItemMixins import DestroyItemMixin
from answerking_app.models.models import Item
from answerking_app.models.serializers import ItemSerializer


class ItemListView(
    mixins.ListModelMixin, CreateMixin, generics.GenericAPIView
):

    queryset: QuerySet = Item.objects.all()
    serializer_class: ItemSerializer = ItemSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class ItemDetailView(
    mixins.RetrieveModelMixin,
    UpdateMixin,
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
        return self.destroy(request, *args, **kwargs)
