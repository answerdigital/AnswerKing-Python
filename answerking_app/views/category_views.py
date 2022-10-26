from django.db.models import QuerySet
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView, csrf_exempt

from answerking_app.models.models import Category, Item
from answerking_app.services import category_service, item_service
from answerking_app.models.validation.serializers import CategorySerializer
from answerking_app.services.service_types.CategoryTypes import CategoryDict
from answerking_app.views.ErrorType import ErrorMessage


class CategoryListView(APIView):
    @csrf_exempt
    def get(self, request: Request, *args, **kwargs) -> Response:
        categories: QuerySet[Category] = category_service.get_all()
        response: list[ReturnDict] = []

        if categories:
            response = [CategorySerializer(cat).data for cat in categories]

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request: Request, *args, **kwargs) -> Response:

        body: CategoryDict = request.data
        created_category: Category | None = category_service.create(body)
        if not created_category:
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

        response: ReturnDict = CategorySerializer(created_category).data

        return Response(response, status=status.HTTP_200_OK)


class CategoryDetailView(APIView):
    @csrf_exempt
    def get(self, request: Request, *args, **kwargs) -> Response:
        category: Category | None = category_service.get_by_id(
            kwargs["cat_id"]
        )

        if not category:
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

        response: ReturnDict = CategorySerializer(category).data

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def put(self, request: Request, *args, **kwargs) -> Response:
        category: Category | None = category_service.get_by_id(
            kwargs["cat_id"]
        )
        if not category:
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

        body: CategoryDict = request.data
        updated_category: Category | None = category_service.update(
            category, body
        )
        if not updated_category:
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

        response: ReturnDict = CategorySerializer(updated_category).data

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def delete(self, request: Request, *args, **kwargs) -> Response:
        category: Category | None = category_service.get_by_id(
            kwargs["cat_id"]
        )
        if not category:
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

        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryItemListView(APIView):
    @csrf_exempt
    def put(self, request: Request, *args, **kwargs) -> Response:
        category: Category | None = category_service.get_by_id(
            kwargs["cat_id"]
        )
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not category or not item:
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

        if item in category.items.all():
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Item already in category",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_400_BAD_REQUEST,
            )

        category.items.add(item)

        response: ReturnDict = CategorySerializer(category).data

        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    def delete(self, request: Request, *args, **kwargs) -> Response:
        category: Category | None = category_service.get_by_id(
            kwargs["cat_id"]
        )
        item: Item | None = item_service.get_by_id(kwargs["item_id"])
        if not category or not item:
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

        if item not in category.items.all():
            error_msg: ErrorMessage = {
                "error": {
                    "message": "Resource update failure",
                    "details": "Item not in category",
                }
            }
            return Response(
                error_msg,
                status=status.HTTP_400_BAD_REQUEST,
            )

        category.items.remove(item)

        response: ReturnDict = CategorySerializer(category).data

        return Response(response, status=status.HTTP_200_OK)
