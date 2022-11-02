from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import OrderLine, Item
from answerking_app.utils.model_types import OrderItemType


class DestroyItemMixin(GenericAPIView):
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        instance: Item = self.get_object()
        existing_orderitems: OrderItemType = OrderLine.objects.filter(
            item=instance.id
        )
        if existing_orderitems:
            return Response(
                {"detail": "Cannot delete, item is in an order."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
