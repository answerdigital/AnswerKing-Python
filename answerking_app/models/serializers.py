import re

from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from rest_framework import serializers

from answerking_app.models.models import Category, Item, Order, OrderLine

MAXNUMBERSIZE = 2147483647


def compress_white_spaces(value: str) -> str:
    return re.sub(" +", " ", value)


class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50,
        allow_blank=False,
        validators=[RegexValidator("^[a-zA-Z !]+$")],
        trim_whitespace=True,
    )
    price = serializers.DecimalField(
        max_digits=19,
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
        trim_whitespace=True,
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
        trim_whitespace=True,
    )
    items = ItemSerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "items")

    def validate_name(self, value: str) -> str:
        return compress_white_spaces(value)


class OrderLineSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="item.id")
    name = serializers.ReadOnlyField(source="item.name")
    price = serializers.ReadOnlyField(source="item.price")
    quantity = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(MAXNUMBERSIZE)]
    )

    class Meta:
        model = OrderLine
        fields = ("id", "name", "price", "quantity", "sub_total")


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="status.status")
    order_items = OrderLineSerializer(source="orderline_set", many=True)
    address = serializers.CharField(
        max_length=200,
        allow_blank=False,
        validators=[RegexValidator("^[a-zA-Z0-9 ,-]+$")],
        trim_whitespace=True,
    )

    def validate_address(self, value: str) -> str:
        return compress_white_spaces(value)

    class Meta:
        model = Order
        fields = (
            "id",
            "address",
            "status",
            "order_items",
            "total",
        )


class ClientOrderLineSerializer(ItemSerializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(MAXNUMBERSIZE)]
    )

    class Meta:
        model = OrderLine
        fields = ("id", "quantity")


class ClientOrderSerializer(serializers.ModelSerializer):
    order_items = ClientOrderLineSerializer(many=True, required=False)
    address = serializers.CharField(
        max_length=200,
        allow_blank=False,
        validators=[RegexValidator("^[a-zA-Z0-9 ,-]+$")],
        trim_whitespace=True,
    )

    def validate_address(self, value: str) -> str:
        return compress_white_spaces(value)

    class Meta:
        model = Order
        fields = ("order_items", "address")


class ClientOrderInfoUpdateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(MAXNUMBERSIZE)],
        required=False,
    )
    status = serializers.CharField(
        max_length=50,
        allow_blank=False,
        validators=[RegexValidator("^[a-zA-Z !]+$")],
        required=False,
    )

    class Meta:
        model = OrderLine
        fields = ("quantity", "status")
