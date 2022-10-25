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


class OrderIncorrectItemQtyType(TypedDict):
    quantity: Any
