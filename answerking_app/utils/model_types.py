from typing import Any

from typing_extensions import (  # for Python <3.11 with (Not)Required
    NotRequired,
    TypedDict,
)


class ProductType(TypedDict):
    id: NotRequired[int]
    name: str
    price: str
    description: str
    retired: NotRequired[bool]


class CategoryType(TypedDict):
    id: NotRequired[int]
    name: NotRequired[str]
    retired: NotRequired[bool]
    products: NotRequired["list[ProductType]"]


class OrderProductType(TypedDict):
    id: NotRequired[int]
    name: NotRequired[str]
    price: NotRequired[str]
    quantity: int
    sub_total: NotRequired[str]


class OrderType(TypedDict):
    id: NotRequired[int]
    address: NotRequired[str]
    order_products: NotRequired["list[OrderProductType]"]
    status: NotRequired[str]
    total: NotRequired[str]


class DetailError(TypedDict):
    detail: NotRequired[str]
    type: str
    title: str
    instance: NotRequired[str]
    errors: NotRequired["str | list[Any] | dict[Any, Any]"]
    status: NotRequired[int]
    traceID: NotRequired[str]
