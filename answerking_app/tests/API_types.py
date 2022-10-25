from typing import TypedDict, Any


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


class OrderItemType(TypedDict):
    id: int
    name: str
    price: str
    quantity: int
    sub_total: str


class NewOrderAddressType(TypedDict):
    address: str


class OrderType(IDType, NewOrderAddressType, TypedDict):
    status: str
    order_items: list[OrderItemType]
    total: str


class OrderItemQtyType(TypedDict):
    quantity: int


class OrderIncorrectItemQtyType(TypedDict):
    quantity: Any
