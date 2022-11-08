from rest_framework.exceptions import APIException


class HttpErrorResponse(APIException):
    def __init__(
        self,
        status: int,
        detail: str | None = None,
        title: str | None = None,
        instance: str | None = None,
        extensions: dict | None = None,
    ):
        super().__init__()
        self.status_code = status
        if detail:
            self.detail = detail
        if title:
            self.title = title
        if instance:
            self.instance = instance
        if extensions:
            self.extensions = extensions
