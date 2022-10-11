import json
from json import JSONDecodeError

from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from answerking_app.services import order_service, item_service
from answerking_app.models.validation.serializers import OrderSerializer


class OrderListView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        orders = order_service.get_all()

        if not orders:
            return HttpResponse(status=204)

        response = [OrderSerializer(order).data for order in orders]

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            if not body:
                return HttpResponse(status=400)
        except JSONDecodeError as e:
            return JsonResponse(
                {
                    "error": {
                        "message": "Failed data validation",
                        "details": f"Invalid JSON in body. {e.msg}",
                    }
                },
                status=400,
            )

        created_order = order_service.create(body)
        if not created_order:
            return JsonResponse(
                {
                    "error": {
                        "message": "Request failed",
                        "details": "Object could not be created",
                    }
                },
                status=400,
            )

        response = OrderSerializer(created_order).data

        return JsonResponse(response, status=200, encoder=DjangoJSONEncoder, safe=False)


class OrderDetailView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        order = order_service.get_by_id(kwargs["order_id"])

        if not order:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        response = OrderSerializer(order).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        order = order_service.get_by_id(kwargs["order_id"])
        if not order:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        try:
            body = json.loads(request.body)
            if not body:
                return HttpResponse(status=400)
        except JSONDecodeError as e:
            return JsonResponse(
                {
                    "error": {
                        "message": "Failed data validation",
                        "details": f"Invalid JSON in body. {e.msg}",
                    }
                },
                status=400,
            )

        updated_order = order_service.update(order, body)
        if not updated_order:
            return JsonResponse(
                {
                    "error": {
                        "message": "Request failed",
                        "details": "Object could not be updated",
                    }
                },
                status=400,
            )

        response = OrderSerializer(updated_order).data

        return JsonResponse(response, status=200, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        order = order_service.get_by_id(kwargs["order_id"])
        if not order:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        order.delete()

        return HttpResponse(status=204)


class OrderItemListView(View):
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        order = order_service.get_by_id(kwargs["order_id"])
        item = item_service.get_by_id(kwargs["item_id"])
        if not order or not item:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        try:
            body = json.loads(request.body)
            if not body:
                return HttpResponse(status=400)
            quantity = body["quantity"]
        except (JSONDecodeError, KeyError) as e:
            return JsonResponse(
                {
                    "error": {
                        "message": "Failed data validation",
                        "details": f"Invalid JSON in body. {e.msg}",
                    }
                },
                status=400,
            )

        order = order_service.add_item(order, item, quantity)
        if not order:
            return JsonResponse(
                {
                    "error": {
                        "message": "Resource update failure",
                        "details": "Failed to add item to order",
                    }
                },
                status=400,
            )

        response = OrderSerializer(order).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        order = order_service.get_by_id(kwargs["order_id"])
        item = item_service.get_by_id(kwargs["item_id"])
        if not order or not item:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        if item not in order.order_items.all():
            return JsonResponse(
                {
                    "error": {
                        "message": "Resource update failure",
                        "details": "Item not in order",
                    }
                },
                status=400,
            )

        order = order_service.remove_item(order, item)
        if not order:
            return JsonResponse(
                {
                    "error": {
                        "message": "Resource update failure",
                        "details": "Failed to delete item from order",
                    }
                },
                status=400,
            )

        response = OrderSerializer(order).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)
