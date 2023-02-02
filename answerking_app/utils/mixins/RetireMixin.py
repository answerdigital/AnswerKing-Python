from django.db.models import QuerySet
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Category, Product, Order, LineItem, Tag
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails


class RetireMixin(GenericAPIView):
    def retire(self, request: Request, *args, **kwargs) -> Response:
        instance: Category | Product | Tag = self.get_object()
        if instance.retired:
            raise ProblemDetails(
                status=status.HTTP_410_GONE,
                detail="This object has already been retired",
            )
        if isinstance(instance, Category):
            instance.retired = True
            instance.save()
        elif isinstance(instance, Product):
            product_active_order_check(instance)
            instance.retired = True
            instance.save()
        elif isinstance(instance, Tag):
            instance.retired = True
            instance.save()
        else:
            raise ParseError
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        return Response(status=status.HTTP_204_NO_CONTENT)


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
