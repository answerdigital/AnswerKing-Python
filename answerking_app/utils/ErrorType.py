from typing import TypedDict


class ErrorMessageContent(TypedDict):
    message: str
    details: str


class ErrorMessage(TypedDict):
    error: ErrorMessageContent
