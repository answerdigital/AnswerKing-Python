import re
from typing import OrderedDict

from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from answerking_app.models.models import (Category, Item, Order, OrderLine,
                                          Status)
from answerking_app.utils.model_types import ItemType

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
    retired = serializers.BooleanField(required=False)

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
    retired = serializers.BooleanField(required=False)

    def create(self, validated_data: dict) -> Category:
        items: list[Item] = self.items_check(validated_data)
        category: Category = Category.objects.create(
            name=validated_data["name"]
        )
        category.items.add(*items)
        return category

    def update(self, category: Category, validated_data: dict) -> Category:
        if "name" in validated_data:
            items: list[Item] = self.items_check(validated_data)
            category.name = validated_data["name"]
            category.items.set(objs=items)
        if "retired" in validated_data:
            category.retired = validated_data["retired"]
        category.save()
        return category

    def items_check(self, validated_data: dict) -> list[Item]:
        items: list[Item] = []
        if "items" in validated_data:
            items_data: list[OrderedDict] = validated_data["items"]
            for item_in_request in items_data:
                item: Item = get_object_or_404(Item, pk=item_in_request["id"])
                items.append(item)
        return items

    class Meta:
        model = Category
        fields = ("id", "name", "items", "retired")

    def validate_name(self, value: str) -> str:
        return compress_white_spaces(value)


class OrderLineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="item.id", required=False)
    name = serializers.ReadOnlyField(source="item.name", required=False)
    price = serializers.DecimalField(
        max_digits=18, decimal_places=2, source="item.price", required=False
    )
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

    def create(self, validated_data: dict) -> Order:
        status: Status
        status, _ = Status.objects.get_or_create(status="Pending")
        address: str = validated_data["address"]
        order: Order = Order.objects.create(
            address=address, status=status, total=0.00
        )
        if "orderline_set" in validated_data:
            order_items_data: list[OrderedDict] = validated_data.pop(
                "orderline_set"
            )
            for order_item in order_items_data:
                item_data: ItemType = order_item.pop("item")
                item: Item = get_object_or_404(Item, pk=item_data["id"])  # type: ignore[reportTypedDictNotRequiredAccess]
                if item.retired:
                    continue
                OrderLine.objects.create(order=order, item=item, **order_item)
        order.calculate_total()
        return order

    def update(self, instance: Order, validated_data: dict) -> Order:
        status_data: dict = validated_data.pop("status", None)
        if status_data:
            instance.status = Status.objects.get(status=status_data["status"])
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance

    def validate_address(self, value: str) -> str:
        return compress_white_spaces(value)

    class Meta:
        model = Order
        fields = "__all__"
