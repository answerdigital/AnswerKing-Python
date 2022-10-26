from django.db.models import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView, csrf_exempt

from answerking_app.models.models import Item, Order
from answerking_app.models.serializers import OrderSerializer
from answerking_app.services import item_service, order_service
from answerking_app.views.ErrorType import ErrorMessage


class OrderListView(APIView):
    @csrf_exempt
    def get(self, request: Request, *args, **kwargs) -> Response:
        orders: QuerySet[Order] = order_service.get_all()
        response: list[ReturnDict] = []

        if orders:
            response = [OrderSerializer(order).data for order in orders]

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request: Request, *args, **kwargs) -> Response:

        created_order: Order | None = order_service.create(request.data)
        if not created_order:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object could not be created",
                }
            }
            return Response(
                error_msg,
                status=400,
            )

        response: ReturnDict = OrderSerializer(created_order).data

        return Response(response, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    @csrf_exempt
    def get(self, request: Request, *args, **kwargs) -> Response:
        order: Order | None = order_service.get_by_id(kwargs["order_id"])

        if not order:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object not found",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_404_NOT_FOUND,
            )

        response: ReturnDict = OrderSerializer(order).data

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def put(self, request: Request, *args, **kwargs) -> Response:
        order: Order | None = order_service.get_by_id(kwargs["order_id"])
        if not order:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object not found",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_404_NOT_FOUND,
            )

        updated_order: Order | None = order_service.update(order, request.data)
        if not updated_order:
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

        response: ReturnDict = OrderSerializer(updated_order).data

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def delete(self, request: Request, *args, **kwargs) -> Response:
        order: Order | None = order_service.get_by_id(kwargs["order_id"])
        if not order:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object not found",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_404_NOT_FOUND,
            )

        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemListView(APIView):
    @csrf_exempt
    def put(self, request: Request, *args, **kwargs) -> Response:
        order: Order | None = order_service.get_by_id(kwargs["order_id"])
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not order or not item:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object not found",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_404_NOT_FOUND,
            )
        order: Order | None = order_service.add_item(order, item, request.data)
        if not order:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Failed to add item to order",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_400_BAD_REQUEST,
            )

        response: ReturnDict = OrderSerializer(order).data

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def delete(self, request: Request, *args, **kwargs) -> Response:
        order: Order | None = order_service.get_by_id(kwargs["order_id"])
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not order or not item:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object not found",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_404_NOT_FOUND,
            )

        if item not in order.order_items.all():
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Item not in order",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_400_BAD_REQUEST,
            )

        order: Order | None = order_service.remove_item(order, item)
        if not order:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Failed to delete item from order",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_400_BAD_REQUEST,
            )

        response: ReturnDict = OrderSerializer(order).data

        return Response(response, status=status.HTTP_200_OK)
