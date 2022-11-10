from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Item, Order
from answerking_app.models.serializers import (
    OrderLineSerializer,
    OrderSerializer,
)
from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


class OrderItemUpdateMixin(UpdateModelMixin):
    def update(
        self, request: Request, order_id: int, item_id: int, *args, **kwargs
    ) -> Response | None:
        order: Order = get_object_or_404(Order, pk=order_id)
        item: Item = get_object_or_404(Item, pk=item_id)

        serialized_body: OrderLineSerializer = OrderLineSerializer(
            data=request.data
        )
        serialized_body.is_valid(raise_exception=True)
        quantity: int = serialized_body.data["quantity"]

        if quantity == 0:
            order.order_items.remove(item)
        elif item not in order.order_items.all():
            order.order_items.add(
                item,
                through_defaults={
                    "quantity": quantity,
                    "sub_total": item.price * quantity,
                },
            )

        else:
            order.orderline_set.filter(item=item.id).update(
                quantity=quantity, sub_total=quantity * item.price
            )
        order.calculate_total()
        serializer: OrderSerializer = OrderSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        response: ReturnDict = serializer.data

        return Response(response, status=status.HTTP_200_OK)


class OrderItemRemoveMixin:
    def remove(
        self, request: Request, order_id: int, item_id: int, *args, **kwargs
    ) -> Response:
        order: Order = get_object_or_404(Order, pk=order_id)
        item: Item = get_object_or_404(Item, pk=item_id)

        if item not in order.order_items.all():
            raise HttpErrorResponse(status=status.HTTP_404_NOT_FOUND)

        updated_order: Order | None = self.remove_item(order, item)

        response: ReturnDict = OrderSerializer(updated_order).data

        return Response(response, status=status.HTTP_200_OK)

    def remove_item(self, order: Order, item: Item) -> Order:
        order.order_items.remove(item)
        order.calculate_total()
        return order
