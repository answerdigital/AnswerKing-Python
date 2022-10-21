from typing import TypedDict

class NewItemType(TypedDict):
    name: str
    price: str
    price: str
    description: str
    stock: int
    calories: int


class ItemIDType(TypedDict):
    id: int


class ItemType(ItemIDType, NewItemType):
    pass