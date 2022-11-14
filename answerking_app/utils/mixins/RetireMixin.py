from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Product, Order
from answerking_app.models.serializers import (
    CategorySerializer,
    ProductSerializer, OrderSerializer,
)
from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse


class RetireMixin(GenericAPIView):
    def retire(self, request: Request, *args, **kwargs) -> Response:
        instance: Category | Product = self.get_object()
        if instance.retired:
            raise HttpErrorResponse(
                status=status.HTTP_400_BAD_REQUEST,
                detail="This object has already been retired",
            )
        instance.retired = True
        instance.save()
        if isinstance(instance, Category):
            response: ReturnDict = CategorySerializer(instance).data
        else:
            response: ReturnDict = ProductSerializer(instance).data
        return Response(response, status=status.HTTP_200_OK)


class CancelOrderMixin(GenericAPIView):
    def cancel_order(self, request: Request, *args, **kwargs) -> Response:
        instance: Order = self.get_object()
        if instance.order_status == 'Cancelled':
            raise HttpErrorResponse(
                status=status.HTTP_400_BAD_REQUEST,
                detail="This order has already been cancelled",
            )
        instance.order_status = 'Cancelled'
        instance.save()
        response: ReturnDict = OrderSerializer(instance).data
        return Response(response, status=status.HTTP_200_OK)
