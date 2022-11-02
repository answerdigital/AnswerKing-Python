from django.db.models import QuerySet
from rest_framework import mixins, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import csrf_exempt

from answerking_app.utils.mixins.GenericMixins import CreateMixin, UpdateMixin
from answerking_app.utils.mixins.ItemMixins import DestroyItemMixin
from answerking_app.models.models import Item
from answerking_app.models.serializers import ItemSerializer


class ItemListView(
    mixins.ListModelMixin, CreateMixin, generics.GenericAPIView
):

    queryset: QuerySet = Item.objects.all()
    serializer_class: ItemSerializer = ItemSerializer

    @csrf_exempt
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    @csrf_exempt
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

    @csrf_exempt
    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)

    @csrf_exempt
    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)
