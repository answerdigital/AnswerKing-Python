from typing import TypedDict


class NewItemType(TypedDict):
    name: str
    price: str
    description: str
    stock: int
    calories: int


class ItemIDType(TypedDict):
    id: int


class ItemType(ItemIDType, NewItemType):
    pass


class CategoryIDType(TypedDict):
    id: int


class NewCategoryType(TypedDict):
    name: str
    items: list[ItemType]


class CategoryType(CategoryIDType, NewCategoryType):
    pass
