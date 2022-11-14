from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Product
from answerking_app.models.serializers import (
    CategorySerializer,
    ProductSerializer,
)


class RetireMixin(GenericAPIView):
    def retire(self, request: Request, *args, **kwargs) -> Response:
        instance: Category | Product = self.get_object()
        instance.retired = True
        instance.save()
        if type(instance) == Category:
            response: ReturnDict = CategorySerializer(instance).data
        else:
            response: ReturnDict = ProductSerializer(instance).data
        return Response(response, status=status.HTTP_200_OK)
