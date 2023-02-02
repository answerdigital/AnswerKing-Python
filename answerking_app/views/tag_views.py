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


class TagListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset: QuerySet = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

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

    def get(self, request: Request, *args, **kwargs) -> Response:
        check_url_parameter(kwargs["pk"])
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs) -> Response:
        check_url_parameter(kwargs["pk"])
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        check_url_parameter(kwargs["pk"])
        return self.retire(request, *args, **kwargs)
