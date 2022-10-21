from typing import TypedDict


class IDType(TypedDict):
    id: int


class NewItemType(TypedDict):
    name: str
    price: str
    description: str
    stock: int
    calories: int


class ItemType(IDType, NewItemType):
    pass


class NewCategoryType(TypedDict):
    name: str
    items: list[ItemType]


class CategoryType(IDType, NewCategoryType):
    pass
