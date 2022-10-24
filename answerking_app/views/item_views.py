import json
from json import JSONDecodeError

from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Item
from answerking_app.services import item_service
from answerking_app.models.validation.serializers import ItemSerializer
from answerking_app.views.ErrorType import ErrorMessage


class ItemListView(View):
    @csrf_exempt
    def get(
        self, request: HttpRequest, *args, **kwargs
    ) -> JsonResponse | HttpResponse:
        items: QuerySet[Item] = item_service.get_all()
        response: list[ReturnDict] = []

        if items:
            response: list[ReturnDict] = [
                ItemSerializer(item).data for item in items
            ]

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def post(
        self, request: HttpRequest, *args, **kwargs
    ) -> JsonResponse | HttpResponse:
        try:
            body: dict | None = json.loads(request.body)
            if not body:
                return HttpResponse(status=400)
        except JSONDecodeError as e:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Failed data validation",
                    "details": f"Invalid JSON in body. {e.msg}",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )

        created_item: Item | None = item_service.create(body)
        if not created_item:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object could not be created",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )

        response: ReturnDict = ItemSerializer(created_item).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)


class ItemDetailView(View):
    @csrf_exempt
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not item:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object not found",
                }
            }
            return JsonResponse(
                error_msg,
                status=404,
            )

        response: ReturnDict = ItemSerializer(item).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def put(
        self, request: HttpRequest, *args, **kwargs
    ) -> JsonResponse | HttpResponse:
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not item:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object not found",
                }
            }
            return JsonResponse(
                error_msg,
                status=404,
            )

        try:
            body: dict | None = json.loads(request.body)
            if not body:
                return HttpResponse(status=400)
        except JSONDecodeError as e:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Failed data validation",
                    "details": f"Invalid JSON in body. {e.msg}",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )

        updated_item: Item | None = item_service.update(item, body)
        if not updated_item:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object could not be updated",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )

        response: ReturnDict = ItemSerializer(updated_item).data

        return JsonResponse(
            response, status=200, encoder=DjangoJSONEncoder, safe=False
        )

    @csrf_exempt
    def delete(
        self, request: HttpRequest, *args, **kwargs
    ) -> JsonResponse | HttpResponse:
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not item:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Object not found",
                }
            }
            return JsonResponse(
                error_msg,
                status=404,
            )

        deleted: bool = item_service.delete(item)
        if not deleted:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Request failed",
                    "details": "Item exists in an order",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )

        return HttpResponse(status=204)
