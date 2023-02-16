from django.db.models import QuerySet
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Product
from answerking_app.models.serializers import (
    ProblemDetailSerializer,
    ProductSerializer,
)
from answerking_app.utils.mixins.RetireMixin import RetireMixin
from answerking_app.utils.schema.schema_examples import (
    problem_detail_example,
    product_body_example,
    product_categories_body_example,
    product_example,
)
from answerking_app.utils.url_parameter_check import check_url_parameter
from answerking_app.models.permissions.auth_permissions import IsStaffUser


class ProductListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Product.objects.all()
    serializer_class: ProductSerializer = ProductSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Inventory"],
        summary="Get all products.",
        responses={
            200: OpenApiResponse(
                response=ProductSerializer,
                description="All the products have been returned.",
                examples=[
                    OpenApiExample(
                        "Product example",
                        value=product_example,
                        response_only=True,
                    )
                ],
            )
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)


class ProductPostView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Product.objects.all()
    serializer_class: ProductSerializer = ProductSerializer
    permission_classes = [IsStaffUser]

    @extend_schema(
        tags=["Inventory"],
        summary="Create a new product.",
        examples=[
            OpenApiExample(
                "Request body", value=product_body_example, request_only=True
            )
        ],
        responses={
            201: OpenApiResponse(
                response=ProductSerializer,
                description="The product has been created.",
                examples=[
                    OpenApiExample(
                        "Product response",
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
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class ProductIdGetView(
    mixins.RetrieveModelMixin
):
    queryset: QuerySet = Product.objects.all()
    serializer_class: ProductSerializer = ProductSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Inventory"],
        summary="Get a single product.",
        responses={
            200: OpenApiResponse(
                response=ProductSerializer,
                description="The product with the provided id has been found.",
                examples=[
                    OpenApiExample(
                        "product response",
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
                description="The product with the given id does not exist.",
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


class ProductUpdateRetireView(
    RetireMixin,
    generics.UpdateAPIView,
):
    queryset: QuerySet = Product.objects.all()
    serializer_class: ProductSerializer = ProductSerializer
    permission_classes = [IsStaffUser]

    @extend_schema(
        tags=["Inventory"],
        summary="Update an existing product",
        examples=[
            OpenApiExample(
                "Request body",
                value=product_categories_body_example,
                request_only=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=ProductSerializer,
                description="The product has been updated.",
                examples=[
                    OpenApiExample(
                        "product response",
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
                description="The product with the given id does not exist.",
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

    @extend_schema(
        tags=["Inventory"],
        summary="Retire an existing product",
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
                description="The product with the given id does not exist.",
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
                description="The product with the given id is already retired.",
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


class ProductView(ProductListView, ProductPostView):
    pass


class ProductIdView(ProductIdGetView, ProductUpdateRetireView):
    pass
