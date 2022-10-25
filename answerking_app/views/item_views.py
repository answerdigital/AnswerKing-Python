from django.db.models import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView, csrf_exempt

from answerking_app.models.models import Item
from answerking_app.models.serializers import ItemSerializer
from answerking_app.services import item_service
from answerking_app.services.service_types.ItemTypes import ItemDict
from answerking_app.views.ErrorType import ErrorMessage


class ItemListView(APIView):
    @csrf_exempt
    def get(self, request: Request, *args, **kwargs) -> Response:
        items: QuerySet[Item] = item_service.get_all()
        response: list[ReturnDict] = []

        if items:
            response: list[ReturnDict] = [
                ItemSerializer(item).data for item in items
            ]

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request: Request, *args, **kwargs) -> Response:

        body: ItemDict = request.data
        created_item: Item | None = item_service.create(body)
        if not created_item:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object could not be created",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_400_BAD_REQUEST,
            )

        response: ReturnDict = ItemSerializer(created_item).data

        return Response(response, status=status.HTTP_200_OK)


class ItemDetailView(APIView):
    @csrf_exempt
    def get(self, request: Request, *args, **kwargs) -> Response:
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not item:
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

        response: ReturnDict = ItemSerializer(item).data

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def put(self, request: Request, *args, **kwargs) -> Response:
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not item:
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

        body: ItemDict = request.data
        updated_item: Item | None = item_service.update(item, body)
        if not updated_item:
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

        response: ReturnDict = ItemSerializer(updated_item).data

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def delete(self, request: Request, *args, **kwargs) -> Response:
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not item:
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

        deleted: bool = item_service.delete(item)
        if not deleted:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Item exists in an order",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
