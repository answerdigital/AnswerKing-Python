from typing import Literal

from django.db.models import QuerySet
from rest_framework import generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Order
from answerking_app.models.serializers import (
    OrderSerializer,
    ProblemDetailSerializer,
)
from answerking_app.utils.mixins.RetireMixin import CancelOrderMixin
from answerking_app.utils.url_parameter_check import check_url_parameter

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from answerking_app.utils.schema.schema_examples import (
    order_example,
    order_body_example,
    problem_detail_example,
)


class OrderListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Order.objects.all()
    serializer_class: OrderSerializer = OrderSerializer

    @extend_schema(
        tags=["Orders"],
        summary="Get all orders.",
        responses={
            200: OpenApiResponse(
                response=OrderSerializer,
                description="All the orders have been returned.",
                examples=[
                    OpenApiExample("Category example", value=order_example)
                ],
            )
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["Orders"],
        summary="Create a new order.",
        examples=[
            OpenApiExample(
                "Request body", value=order_body_example, request_only=True
            )
        ],
        responses={
            201: OpenApiResponse(
                response=OrderSerializer,
                description="The order has been created.",
                examples=[
                    OpenApiExample(
                        "Order response",
                        value=order_example,
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
        return self.create(request)


class OrderDetailView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    CancelOrderMixin,
    generics.GenericAPIView,
):

    queryset: QuerySet = Order.objects.all()
    serializer_class: OrderSerializer = OrderSerializer
    lookup_url_kwarg: Literal["pk"] = "pk"

    @extend_schema(
        tags=["Orders"],
        summary="Get a single order.",
        responses={
            200: OpenApiResponse(
                response=OrderSerializer,
                description="The order with the provided id has been found.",
                examples=[
                    OpenApiExample(
                        "Order response",
                        value=order_example,
                        response_only=True,
                    )
                ],
            ),
            404: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="The order with the given id does not exist.",
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

    @extend_schema(
        tags=["Orders"],
        summary="Update an existing order.",
        examples=[
            OpenApiExample(
                "Request body",
                value=order_body_example,
                request_only=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=OrderSerializer,
                description="The order has been updated.",
                examples=[
                    OpenApiExample(
                        "Order response",
                        value=order_example,
                        response_only=True,
                    )
                ],
            ),
            400: OpenApiResponse(
                response=ProblemDetailSerializer,
                description="When invalid parameters are provided.",
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
                description="When the category with the given id does not exist.",
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
        tags=["Orders"],
        summary="Cancel an existing order",
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
                description="The order with the given id does not exist.",
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
        return self.cancel_order(request, *args, **kwargs)
