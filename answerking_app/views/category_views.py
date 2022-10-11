import json
from json import JSONDecodeError

from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from answerking_app.services import category_service, item_service
from answerking_app.models.validation.serializers import CategorySerializer


class CategoryListView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        categories = category_service.get_all()
        if not categories:
            return HttpResponse(status=204)

        response = [CategorySerializer(cat).data for cat in categories]

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

        created_category = category_service.create(body)
        if not created_category:
            return JsonResponse(
                {
                    "error": {
                        "message": "Request failed",
                        "details": "Object could not be created",
                    }
                },
                status=400,
            )

        response = CategorySerializer(created_category).data

        return JsonResponse(response, status=200, encoder=DjangoJSONEncoder, safe=False)


class CategoryDetailView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        category = category_service.get_by_id(kwargs["cat_id"])

        if not category:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        response = CategorySerializer(category).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        category = category_service.get_by_id(kwargs["cat_id"])
        if not category:
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

        updated_category = category_service.update(category, body)
        if not updated_category:
            return JsonResponse(
                {
                    "error": {
                        "message": "Request failed",
                        "details": "Object could not be updated",
                    }
                },
                status=400,
            )

        response = CategorySerializer(updated_category).data

        return JsonResponse(response, status=200, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        category = category_service.get_by_id(kwargs["cat_id"])
        if not category:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        category.delete()

        return HttpResponse(status=204)


class CategoryItemListView(View):
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        category = category_service.get_by_id(kwargs["cat_id"])
        item = item_service.get_by_id(kwargs["item_id"])
        if not category or not item:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        if item in category.items.all():
            return JsonResponse(
                {
                    "error": {
                        "message": "Resource update failure",
                        "details": "Item already in category",
                    }
                },
                status=400,
            )

        category.items.add(item)

        response = CategorySerializer(category).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        category = category_service.get_by_id(kwargs["cat_id"])
        item = item_service.get_by_id(kwargs["item_id"])
        if not category or not item:
            return JsonResponse(
                {"error": {"message": "Request failed", "details": "Object not found"}},
                status=404,
            )

        if item not in category.items.all():
            return JsonResponse(
                {
                    "error": {
                        "message": "Resource update failure",
                        "details": "Item not in category",
                    }
                },
                status=400,
            )

        category.items.remove(item)

        response = CategorySerializer(category).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)
