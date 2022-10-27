import re

from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from rest_framework import serializers
from typing_extensions import Required

from answerking_app.models.models import Category, Item, Order, OrderLine

MAXNUMBERSIZE = 2147483647


def compress_white_spaces(value: str) -> str:
    return re.sub(" +", " ", value)


class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(
        max_length=50,
        allow_blank=False,
        validators=[RegexValidator("^[a-zA-Z !]+$")],
    )
    price = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(MAXNUMBERSIZE)],
    )
    description = serializers.CharField(
        max_length=200,
        allow_null=True,
        allow_blank=True,
        validators=[
            RegexValidator(
                "^[a-zA-Z .!,#]+$",
            )
        ],
    )
    stock = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(MAXNUMBERSIZE)]
    )
    calories = serializers.IntegerField(
        validators=[MinValueValidator(0)],
        allow_null=True,
    )

    class Meta:
        model = Item
        fields = "__all__"

    def validate_name(self, value: str) -> str:
        return compress_white_spaces(value)

    def validate_description(self, value: str) -> str:
        return compress_white_spaces(value)


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50,
        allow_blank=False,
        validators=[RegexValidator("^[a-zA-Z !]+$")],
    )
    items = ItemSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = ("id", "name", "items")

    def validate_name(self, value: str) -> str:
        return compress_white_spaces(value)


class OrderLineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="item.id", required=False)
    name = serializers.ReadOnlyField(source="item.name", required=False)
    price = serializers.ReadOnlyField(source="item.price", required=False)
    quantity = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(MAXNUMBERSIZE)],
    )

    class Meta:
        model = OrderLine
        fields = ("id", "name", "price", "quantity", "sub_total")


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="status.status", required=False)
    order_items = OrderLineSerializer(
        source="orderline_set", many=True, required=False
    )
    address = serializers.CharField(
        max_length=200,
        allow_blank=False,
        validators=[RegexValidator("^[a-zA-Z0-9 ,-]+$")],
        required=False,
    )

    def validate_address(self, value: str) -> str:
        return compress_white_spaces(value)

    class Meta:
        model = Order
        fields = "__all__"
