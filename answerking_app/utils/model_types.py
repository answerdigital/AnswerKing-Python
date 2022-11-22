import datetime

from typing_extensions import (  # for Python <3.11 with (Not)Required
    NotRequired,
    TypedDict,
)
from decimal import Decimal

from typing import Any


class ProductType(TypedDict):
    id: NotRequired[int]
    name: str
    price: str | float
    description: str
    categories: NotRequired["list[CategoryType]"]
    retired: NotRequired[bool]


class CategoryProductType(TypedDict):
    id: int


class CategoryType(TypedDict):
    id: NotRequired[int]
    name: NotRequired[str]
    description: NotRequired[str]
    createdOn: NotRequired[datetime.datetime | str]
    lastUpdated: NotRequired[datetime.datetime | str]
    retired: NotRequired[bool]
    products: NotRequired["list[CategoryProductType]"]


class OrderProductType(TypedDict):
    id: NotRequired[int]
    quantity: int
    sub_total: NotRequired[str]


class OrderType(TypedDict):
    id: NotRequired[int]
    order_status: NotRequired[str]
    order_total: NotRequired[Decimal]
    created_on: NotRequired[datetime.datetime]
    last_updated: NotRequired[datetime.datetime]
    line_items: NotRequired["list[OrderProductType]"]


class OrderProductTypeApiFormat(TypedDict):
    product: ProductType
    quantity: int
    subTotal: NotRequired[float]


class OrderTypeApiFormat(TypedDict):
    id: NotRequired[int]
    orderStatus: NotRequired[str]
    orderTotal: NotRequired[float]
    createdOn: NotRequired[datetime.datetime | str]
    lastUpdated: NotRequired[datetime.datetime | str]
    lineItems: NotRequired["list[OrderProductTypeApiFormat]"]


class DetailError(TypedDict):
    detail: NotRequired[str]
    type: str
    title: str
    instance: NotRequired[str]
    errors: NotRequired["str | list[Any] | dict[Any, Any]"]
    status: NotRequired[int]
    traceID: NotRequired[str]
