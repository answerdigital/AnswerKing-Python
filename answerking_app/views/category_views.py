from django.db.models import QuerySet
from rest_framework import generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Category
from answerking_app.models.serializers import (
    CategorySerializer,
    ProblemDetailSerializer,
)
from answerking_app.utils.mixins.CategoryProductMixins import (
    CategoryProductListMixin,
)
from answerking_app.utils.mixins.RetireMixin import RetireMixin
from answerking_app.utils.url_parameter_check import check_url_parameter

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)
from answerking_app.utils.schema.schema_examples import (
    category_example,
    category_body_example,
    problem_detail_example,
    category_products_body_example,
    product_example,
)


# classes for each endpoint and type of request

class CategoryGetView(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    permission_classes = []
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    @extend_schema(
        tags=["Inventory"],
        summary="Get all categories.",
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                description="All the categories have been returned.",
                examples=[
                    OpenApiExample(
                        "Category example",
                        value=category_example,
                        response_only=True,
                    )
                ],
            )
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)


class CategoryPostView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    permission_classes = []
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    @extend_schema(
        tags=["Inventory"],
        summary="Create a new category.",
        examples=[
            OpenApiExample(
                "Request body", value=category_body_example, request_only=True
            )
        ],
        responses={
            201: OpenApiResponse(
                response=CategorySerializer,
                description="The category has been created.",
                examples=[
                    OpenApiExample(
                        "Category response",
                        value=category_example,
                        response_only=True,
                    )
                ],
            ),
            400: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="Invalid parameters are provided.",
                examples=[
                    OpenApiExample(
                        "Problem response",
                        value=problem_detail_example,
                        response_only=True,
                    )
                ],
            ),
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class CategoryIdGetView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    permission_classes = []
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    @extend_schema(
        tags=["Inventory"],
        summary="Get a single category.",
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                description="Category with the provided id has been found.",
                examples=[
                    OpenApiExample(
                        "Category response",
                        value=category_example,
                        response_only=True,
                    )
                ],
            ),
            400: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="Invalid parameters are provided.",
                examples=[
                    OpenApiExample(
                        "Problem response",
                        value=problem_detail_example,
                        response_only=True,
                    )
                ],
            ),
            404: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="Category with the given id does not exist.",
                examples=[
                    OpenApiExample(
                        "Problem response",
                        value=problem_detail_example,
                        response_only=True,
                    )
                ],
            ),
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        check_url_parameter(kwargs["pk"])
        return self.retrieve(request, *args, **kwargs)


class CategoryIdPutView(
        mixins.UpdateModelMixin,
        generics.GenericAPIView,
):
    permission_classes = []
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    @extend_schema(
        tags=["Inventory"],
        summary="Update an existing category",
        examples=[
            OpenApiExample(
                "Request body",
                value=category_products_body_example,
                request_only=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                description="The category has been updated.",
                examples=[
                    OpenApiExample(
                        "Category response",
                        value=category_example,
                        response_only=True,
                    )
                ],
            ),
            400: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="Invalid parameters are provided.",
                examples=[
                    OpenApiExample(
                        "Problem response",
                        value=problem_detail_example,
                        response_only=True,
                    )
                ],
            ),
            404: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="Category with the given id does not exist.",
                examples=[
                    OpenApiExample(
                        "Problem response",
                        value=problem_detail_example,
                        response_only=True,
                    )
                ],
            ),
        },
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        check_url_parameter(kwargs["pk"])
        return self.update(request, *args, **kwargs)


class CategoryIdDeleteView(
    RetireMixin,
    generics.GenericAPIView,
):
    permission_classes = []
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer
    @extend_schema(
        tags=["Inventory"],
        summary="Retire an existing category",
        responses={
            204: OpenApiResponse(description="No Content."),
            400: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="Invalid parameters are provided.",
                examples=[
                    OpenApiExample(
                        "Problem response",
                        value=problem_detail_example,
                        response_only=True,
                    )
                ],
            ),
            404: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="Category with the given id does not exist.",
                examples=[
                    OpenApiExample(
                        "Problem response",
                        value=problem_detail_example,
                        response_only=True,
                    )
                ],
            ),
            410: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="Category with the given id is already retired.",
                examples=[
                    OpenApiExample(
                        "Problem response",
                        value=problem_detail_example,
                        response_only=True,
                    )
                ],
            ),
        },
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        check_url_parameter(kwargs["pk"])
        return self.retire(request, *args, **kwargs)


class CategoryProductGetView(
    CategoryProductListMixin,
    generics.GenericAPIView,
):
    permission_classes = []
    queryset: QuerySet = Category.objects.all()
    serializer_class: CategorySerializer = CategorySerializer

    @extend_schema(
        tags=["Inventory"],
        summary="Get all products in a category.",
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                description="When all the products have been returned.",
                examples=[
                    OpenApiExample(
                        "Category response",
                        value=product_example,
                        response_only=True,
                    )
                ],
            ),
            400: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="Invalid parameters are provided.",
                examples=[
                    OpenApiExample(
                        "Problem response",
                        value=problem_detail_example,
                        response_only=True,
                    )
                ],
            ),
            404: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="Category with the given id does not exist.",
                examples=[
                    OpenApiExample(
                        "Problem response",
                        value=problem_detail_example,
                        response_only=True,
                    )
                ],
            ),
        },
    )
    def get(self, request: Request, **kwargs) -> Response:
        check_url_parameter(kwargs["pk"])
        return self.list(**kwargs)


# classes grouping all the requests for one endpoint

class CategoryView(
    CategoryGetView,
    CategoryPostView
):
    pass


class CategoryIdView(
    CategoryIdGetView,
    CategoryIdPutView,
    CategoryIdDeleteView
):
    pass


class CategoryProductView(
    CategoryProductGetView
):
    pass

