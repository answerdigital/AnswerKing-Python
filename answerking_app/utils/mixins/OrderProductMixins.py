from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Product, Order
from answerking_app.models.serializers import (
    OrderLineSerializer,
    OrderSerializer,
)
from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


class OrderProductUpdateMixin(UpdateModelMixin):
    def update(
        self, request: Request, order_id: int, product_id: int, *args, **kwargs
    ) -> Response | None:
        order: Order = get_object_or_404(Order, pk=order_id)
        product: Product = get_object_or_404(Product, pk=product_id)

        serialized_body: OrderLineSerializer = OrderLineSerializer(
            data=request.data
        )
        serialized_body.is_valid(raise_exception=True)
        quantity: int = serialized_body.data["quantity"]

        if quantity == 0:
            order.line_items.remove(product)
        elif product not in order.line_items.all():
            order.line_items.add(
                product,
                through_defaults={
                    "quantity": quantity,
                    "sub_total": product.price * quantity,
                },
            )

        else:
            order.orderline_set.filter(product=product.id).update(
                quantity=quantity, sub_total=quantity * product.price
            )
        order.calculate_total()
        serializer: OrderSerializer = OrderSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        response: ReturnDict = serializer.data

        return Response(response, status=status.HTTP_200_OK)


class OrderProductRemoveMixin:
    def remove(
        self, request: Request, order_id: int, product_id: int, *args, **kwargs
    ) -> Response:
        order: Order = get_object_or_404(Order, pk=order_id)
        product: Product = get_object_or_404(Product, pk=product_id)

        if product not in order.line_items.all():
            raise HttpErrorResponse(status=status.HTTP_404_NOT_FOUND)

        updated_order: Order | None = self.remove_product(order, product)

        response: ReturnDict = OrderSerializer(updated_order).data

        return Response(response, status=status.HTTP_200_OK)

    def remove_product(self, order: Order, product: Product) -> Order:
        order.line_items.remove(product)
        order.calculate_total()
        return order
