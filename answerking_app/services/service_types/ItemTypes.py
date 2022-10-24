from typing import TypedDict
from decimal import Decimal


class ItemDict(TypedDict):
    name: str
    price: Decimal
    description: str
    stock: int
    calories: int


class ItemWithIDDict(TypedDict):
    id: int
    name: str
    price: Decimal
    description: str
    stock: int
    calories: int
