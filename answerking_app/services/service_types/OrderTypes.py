from typing import TypedDict


class OrderItems(TypedDict):
    id: int
    quantity: int


class OrderCreateDict(TypedDict):
    address: str
    order_items: list[OrderItems]


class OrderUpdateDict(TypedDict):
    address: str
    status: str


class QuantityUpdateDict(TypedDict):
    quantity: int
