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
    retired: bool


class NewCategoryName(TypedDict):
    name: str


class NewCategoryItems(TypedDict):
    items: list[ItemType]


class NewCategoryType(NewCategoryName, NewCategoryItems):
    pass


class CategoryType(IDType, NewCategoryType):
    retired: bool


class OrderItemType(TypedDict):
    id: int
    name: str
    price: str
    quantity: int
    sub_total: str


class NewOrderAddressType(TypedDict):
    address: str


class NewOrderType(NewOrderAddressType, TypedDict):
    order_items: list[OrderItemType]


class NewStatusType(TypedDict):
    status: str


class UpdateOrderType(NewOrderAddressType, NewStatusType):
    pass


class OrderType(IDType, NewOrderType, NewStatusType, TypedDict):
    total: str


class OrderItemQtyType(TypedDict):
    quantity: int


class DetailError(TypedDict):
    detail: str


class QuantityError(TypedDict):
    quantity: list
