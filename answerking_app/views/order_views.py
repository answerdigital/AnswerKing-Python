import json
from json import JSONDecodeError

from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Order, Item
from answerking_app.services import order_service, item_service
from answerking_app.models.validation.serializers import OrderSerializer
from answerking_app.views.ErrorType import ErrorMessage


class OrderListView(View):
    @csrf_exempt
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse | HttpResponse:
        orders: QuerySet[Order] = order_service.get_all()

        if not orders:
            return HttpResponse(status=204)

        response: list[ReturnDict] = [OrderSerializer(order).data for order in orders]

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

        created_order: Order | None = order_service.create(body)
        if not created_order:
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

        response: ReturnDict = OrderSerializer(created_order).data

        return JsonResponse(response, status=200, encoder=DjangoJSONEncoder, safe=False)


class OrderDetailView(View):
    @csrf_exempt
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        order: Order | None = order_service.get_by_id(kwargs["order_id"])

        if not order:
            error_msg: ErrorMessage = {
                "error": {"message": "Request failed", "details": "Object not found"}
            }
            return JsonResponse(
                error_msg,
                status=404,
            )

        response: ReturnDict = OrderSerializer(order).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def put(self, request: HttpRequest, *args, **kwargs) -> JsonResponse | HttpResponse:
        order: Order | None = order_service.get_by_id(kwargs["order_id"])
        if not order:
            error_msg: ErrorMessage = {
                "error": {"message": "Request failed", "details": "Object not found"}
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

        updated_order: Order | None = order_service.update(order, body)
        if not updated_order:
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

        response: ReturnDict = OrderSerializer(updated_order).data

        return JsonResponse(response, status=200, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def delete(
        self, request: HttpRequest, *args, **kwargs
    ) -> JsonResponse | HttpResponse:
        order: Order | None = order_service.get_by_id(kwargs["order_id"])
        if not order:
            error_msg: ErrorMessage = {
                "error": {"message": "Request failed", "details": "Object not found"}
            }
            return JsonResponse(
                error_msg,
                status=404,
            )

        order.delete()

        return HttpResponse(status=204)


class OrderItemListView(View):
    @csrf_exempt
    def put(self, request: HttpRequest, *args, **kwargs) -> JsonResponse | HttpResponse:
        order: Order | None = order_service.get_by_id(kwargs["order_id"])
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not order or not item:
            error_msg: ErrorMessage = {
                "error": {"message": "Request failed", "details": "Object not found"}
            }
            return JsonResponse(
                error_msg,
                status=404,
            )

        try:
            body: dict | None = json.loads(request.body)
            if not body:
                return HttpResponse(status=400)
            quantity: int = body["quantity"]
        except KeyError as e:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Failed data validation",
                    "details": f"'quantity' not found in json body.",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )
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

        order: Order | None = order_service.add_item(order, item, quantity)
        if not order:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Failed to add item to order",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )

        response: ReturnDict = OrderSerializer(order).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def delete(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        order: Order | None = order_service.get_by_id(kwargs["order_id"])
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not order or not item:
            error_msg: ErrorMessage = {
                "error": {"message": "Request failed", "details": "Object not found"}
            }
            return JsonResponse(
                error_msg,
                status=404,
            )

        if item not in order.order_items.all():
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Item not in order",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )

        order: Order | None = order_service.remove_item(order, item)
        if not order:
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Failed to delete item from order",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )

        response: ReturnDict = OrderSerializer(order).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)
