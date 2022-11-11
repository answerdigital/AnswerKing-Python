from rest_framework.mixins import UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response


class RetireMixin(UpdateModelMixin):
    def retire(self, request: Request, *args, **kwargs) -> Response:
        request.data["retired"] = True
        return super().partial_update(request, *args, **kwargs)
