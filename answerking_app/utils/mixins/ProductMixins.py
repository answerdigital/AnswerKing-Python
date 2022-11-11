from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Product, OrderLine
from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse
from answerking_app.utils.model_types import OrderProductType


class DestroyProductMixin(GenericAPIView):
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        instance: Product = self.get_object()
        existing_orderproducts: OrderProductType = OrderLine.objects.filter(
            product=instance.id
        )
        if existing_orderproducts:
            raise HttpErrorResponse(status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
