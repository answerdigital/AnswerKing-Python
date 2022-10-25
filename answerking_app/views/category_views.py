import json
from json import JSONDecodeError

from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Item
from answerking_app.services import category_service, item_service
from answerking_app.models.validation.serializers import CategorySerializer
from answerking_app.views.ErrorType import ErrorMessage


class CategoryListView(View):
    @csrf_exempt
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse | HttpResponse:
        categories: QuerySet[Category] = category_service.get_all()
        response: list[ReturnDict] = []

        if categories:
            response = [CategorySerializer(cat).data for cat in categories]

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

        created_category: Category | None = category_service.create(body)
        if not created_category:
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

        response: ReturnDict = CategorySerializer(created_category).data

        return JsonResponse(response, status=200, encoder=DjangoJSONEncoder, safe=False)


class CategoryDetailView(View):
    @csrf_exempt
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        category: Category | None = category_service.get_by_id(kwargs["cat_id"])

        if not category:
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

        response: ReturnDict = CategorySerializer(category).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def put(self, request: HttpRequest, *args, **kwargs) -> JsonResponse | HttpResponse:
        category: Category | None = category_service.get_by_id(kwargs["cat_id"])
        if not category:
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

        updated_category: Category | None = category_service.update(category, body)
        if not updated_category:
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

        response: ReturnDict = CategorySerializer(updated_category).data

        return JsonResponse(response, status=200, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def delete(
        self, request: HttpRequest, *args, **kwargs
    ) -> JsonResponse | HttpResponse:
        category: Category | None = category_service.get_by_id(kwargs["cat_id"])
        if not category:
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

        category.delete()

        return HttpResponse(status=204)


class CategoryItemListView(View):
    @csrf_exempt
    def put(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        category: Category | None = category_service.get_by_id(kwargs["cat_id"])
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not category or not item:
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

        if item in category.items.all():
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Item already in category",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )

        category.items.add(item)

        response: ReturnDict = CategorySerializer(category).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

    @csrf_exempt
    def delete(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        category: Category | None = category_service.get_by_id(kwargs["cat_id"])
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not category or not item:
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

        if item not in category.items.all():
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Item not in category",
                }
            }
            return JsonResponse(
                error_msg,
                status=400,
            )

        category.items.remove(item)

        response: ReturnDict = CategorySerializer(category).data

        return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)
