import json
from json import JSONDecodeError

from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from answerking_app.services import item_service
from answerking_app.models.validation.serializers import ItemSerializer


class ItemListView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        items = item_service.get_all()
        if not items:
            return HttpResponse(status=204)

        response = [ItemSerializer(item).data for item in items]

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

        created_item = item_service.create(body)
        if not created_item:
            return JsonResponse(
                {
                    "error": {
                        "message": "Request failed",
                        "details": "Object could not be created",
                    }
                },
                status=400,
            )

        response = ItemSerializer(created_item).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)


class ItemDetailView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        item = item_service.get_by_id(kwargs["item_id"])
        if not item:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        response = ItemSerializer(item).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        item = item_service.get_by_id(kwargs["item_id"])
        if not item:
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

        updated_item = item_service.update(item, body)
        if not updated_item:
            return JsonResponse(
                {
                    "error": {
                        "message": "Request failed",
                        "details": "Object could not be updated",
                    }
                },
                status=400,
            )

        response = ItemSerializer(updated_item).data

        return JsonResponse(response, status=200, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        item = item_service.get_by_id(kwargs["item_id"])
        if not item:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        deleted = item_service.delete(item)
        if not deleted:
            return JsonResponse(
                {
                    "error": {
                        "message": "Request failed",
                        "details": "Item exists in an order",
                    }
                },
                status=400,
            )

        return HttpResponse(status=204)
