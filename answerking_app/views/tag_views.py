from django.db.models import QuerySet
from rest_framework import generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Tag
from answerking_app.models.serializers import (
    TagSerializer,
    ProblemDetailSerializer,
)
from answerking_app.utils.mixins.RetireMixin import RetireMixin
from answerking_app.utils.url_parameter_check import check_url_parameter

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)
from answerking_app.utils.schema.schema_examples import (
    tag_example,
    retired_tag_example,
    problem_detail_example, tag_body_example,
)

class TagListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset: QuerySet = Tag.objects.all()
    serializer_class = TagSerializer

    @extend_schema(
        tags=["tags"],
        summary="Get all tags.",
        responses={
            200: OpenApiResponse(
                response=TagSerializer,
                description="All the tags have been returned.",
                examples=[
                    OpenApiExample(
                        "Tag example",
                        value=tag_example,
                        response_only=True
                    )
                ],
            )
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["tags"],
        summary="Create an new tag.",
        examples=[
            OpenApiExample(
                "Request body",
                value=tag_body_example,
                request_only=True
            )
        ],
        responses={
            201: OpenApiResponse(
                response=TagSerializer,
                description="Tag created.",
                examples=[
                    OpenApiExample(
                        "Tag response",
                        value=tag_example,
                        request_only=True,
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
                ]
            )
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class TagDetailView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    RetireMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Tag.objects.all()
    serializer_class: TagSerializer = TagSerializer

    @extend_schema(
        tags=["tags"],
        summary="Get a single tag.",
        responses={
            200: OpenApiResponse(
                response=TagSerializer,
                description="Tag with the provided id has been found.",
                examples=[
                    OpenApiExample(
                        "Tag example",
                        value=tag_example,
                        response_only=True
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
                description="The tag with the given id does not exist.",
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
        tags=["tags"],
        summary="Update an existing tag",
        examples=[
            OpenApiExample(
                "Request body",
                value=tag_body_example,
                request_only=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=TagSerializer,
                description="The tag has been updated.",
                examples=[
                    OpenApiExample(
                        "Tag example",
                        value=tag_example,
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
                description="The tag with the given id does not exist.",
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
        tags=["tags"],
        summary="Retire an existing tag",
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
                description="The tag with the given id does not exist.",
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
                description="The tag with the given id is already retired.",
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
