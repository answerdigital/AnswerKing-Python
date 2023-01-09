from django.db.models import QuerySet
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Product, Order, LineItem
from answerking_app.models.serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
)
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails


class RetireMixin(GenericAPIView):
    def retire(self, request: Request, *args, **kwargs) -> Response:
        instance: Category | Product = self.get_object()
        if instance.retired:
            raise ProblemDetails(
                status=status.HTTP_410_GONE,
                detail="This object has already been retired",
            )
        if isinstance(instance, Category):
            instance.retired = True
            instance.save()
            response: ReturnDict = CategorySerializer(instance).data
        elif isinstance(instance, Product):
            product_active_order_check(instance)
            instance.retired = True
            instance.save()
            response: ReturnDict = ProductSerializer(instance).data
        else:
            raise ParseError
        return Response(response, status=status.HTTP_200_OK)


class CancelOrderMixin(GenericAPIView):
    def cancel_order(self, request: Request, *args, **kwargs) -> Response:
        instance: Order = self.get_object()
        if instance.order_status == "Cancelled":
            raise ProblemDetails(
                status=status.HTTP_400_BAD_REQUEST,
                detail="This order has already been cancelled",
            )
        instance.order_status = "Cancelled"
        instance.save()
        response: ReturnDict = OrderSerializer(instance).data
        return Response(response, status=status.HTTP_200_OK)


def product_active_order_check(instance: Product):
    existing_order_products: QuerySet[LineItem] = LineItem.objects.filter(
        product=instance.id
    )
    for order_product in existing_order_products:
        if order_product.order.order_status == "Created":
            raise ProblemDetails(
                status=status.HTTP_400_BAD_REQUEST,
                detail="This product is in an active order",
            )
