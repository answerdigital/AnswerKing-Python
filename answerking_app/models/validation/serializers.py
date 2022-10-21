from decimal import Decimal

import typing
from rest_framework import serializers
from answerking_app.models.models import Order, OrderLine, Item, Category
from answerking_app.models.validation.validators import (
    validate_name_string,
    validate_descriptive_string,
    validate_address_string,
    validate_positive_number,
    validate_price,
)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "price", "description", "stock", "calories")

    def validate_name(self, value: str | None) -> str:
        return validate_name_string(value)

    def validate_price(self, value: typing.Any) -> Decimal:
        return validate_price(value)

    def validate_description(self, value: str | None) -> str:
        return validate_descriptive_string(value)

    def validate_stock(self, value: typing.Any) -> int:
        return validate_positive_number(value)

    def validate_calories(self, value: typing.Any) -> int:
        return validate_positive_number(value)


class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "items")

    def validate_name(self, value: str) -> str:
        return validate_name_string(value)


class OrderLineSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="item.id")
    name = serializers.ReadOnlyField(source="item.name")
    price = serializers.ReadOnlyField(source="item.price")
    # item = ItemSerializer()

    class Meta:
        model = OrderLine
        fields = ("id", "name", "price", "quantity", "sub_total")

    def validate_quantity(self, value: typing.Any) -> int:
        return validate_positive_number(value)


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="status.status")
    order_items = OrderLineSerializer(source="orderline_set", many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "address",
            "status",
            "order_items",
            "total",
        )

    def validate_address(self, value) -> str:
        return validate_address_string(value)
