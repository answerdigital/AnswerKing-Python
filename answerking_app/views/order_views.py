from typing import Literal

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from rest_framework import mixins, generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import csrf_exempt

from answerking_app.utils.mixins.OrderItemMixins import (
    OrderItemUpdateMixin,
    OrderItemRemoveMixin,
)

from answerking_app.models.models import Order
from answerking_app.models.serializers import OrderSerializer
from answerking_app.utils.ErrorType import ErrorMessage


class OrderListView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset: QuerySet = Order.objects.all()
    serializer_class: OrderSerializer = OrderSerializer

    @csrf_exempt
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request)


class OrderDetailView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):

    queryset: QuerySet = Order.objects.all()
    serializer_class: OrderSerializer = OrderSerializer
    lookup_url_kwarg: Literal["order_id"] = "order_id"

    @csrf_exempt
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    @csrf_exempt
    def put(self, request: Request, *args, **kwargs) -> Response:
        try:
            return self.partial_update(request, *args, **kwargs)
        except (KeyError, ObjectDoesNotExist):
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object could not be updated",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @csrf_exempt
    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)


class OrderItemListView(
    OrderItemUpdateMixin, OrderItemRemoveMixin, generics.GenericAPIView
):
    serializer_class: OrderSerializer = OrderSerializer

    @csrf_exempt
    def put(
        self, request: Request, order_id: int, item_id: int, *args, **kwargs
    ) -> Response:
        return self.update(request, order_id, item_id, *args, **kwargs)

    @csrf_exempt
    def delete(
        self, request: Request, order_id: int, item_id: int, *args, **kwargs
    ) -> Response:
        return self.remove(request, order_id, item_id, *args, **kwargs)
