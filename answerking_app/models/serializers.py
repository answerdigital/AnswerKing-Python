import re
from typing import OrderedDict

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from rest_framework import serializers, status

from answerking_app.models.models import (
    Category,
    Product,
    Order,
    OrderLine,
)
from answerking_app.utils.get_object_or_400 import get_object_or_400
from answerking_app.utils.mixins.ApiExceptions import HttpErrorResponse

MAXNUMBERSIZE = 2147483647


def compress_white_spaces(value: str) -> str:
    return re.sub(" +", " ", value)


class CategoryDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(
        max_length=50,
        allow_blank=False,
        validators=[RegexValidator("^[a-zA-Z !]+$")],
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

    def create(self, validated_data: dict) -> Category:
        products: list[Product] = self.products_check(validated_data)
        category: Category = Category.objects.create(
            name=validated_data["name"],
            description=validated_data["description"],
        )
        category.products.add(*products)
        return category

    def update(self, category: Category, validated_data: dict) -> Category:
        if category.retired:
            raise HttpErrorResponse(
                status=status.HTTP_410_GONE,
                detail="This category has been retired",
            )
        products: list[Product] = self.products_check(validated_data)
        category.name = validated_data["name"]
        category.description = validated_data["description"]
        category.products.set(objs=products)
        category.save()
        return category

    def products_check(self, validated_data: dict) -> list[Product]:
        products: list[Product] = []
        if "products" in validated_data:
            products_id_list: list[int] = [
                prod["id"] for prod in validated_data["products"]
            ]
            for product_id in products_id_list:
                product: Product = get_object_or_400(Product, pk=product_id)
                if product.retired:
                    raise HttpErrorResponse(
                        status=status.HTTP_410_GONE,
                        detail="This product has been retired",
                    )
                products.append(product)
        return products

    class Meta:
        model = Category
        fields = ("id", "name", "description")

    def validate_name(self, value: str) -> str:
        return compress_white_spaces(value)


class ProductSerializer(serializers.ModelSerializer):
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
    categories = CategoryDetailSerializer(
        source="category_set", many=True, required=False
    )
    retired = serializers.BooleanField(required=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "categories",
            "retired",
        )

    def validate_name(self, value: str) -> str:
        return compress_white_spaces(value)

    def validate_description(self, value: str) -> str:
        return compress_white_spaces(value)


class ProductDetailSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ["id"]


class CategorySerializer(CategoryDetailSerializer):
    createdOn = serializers.DateTimeField(source="created_on", read_only=True)
    lastUpdated = serializers.DateTimeField(
        source="last_updated", read_only=True
    )
    products = ProductDetailSerializer(many=True)
    retired = serializers.BooleanField(required=False)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "description",
            "createdOn",
            "lastUpdated",
            "products",
            "retired",
        )


class ProductSerializerReadOnly(serializers.ModelSerializer):
    id = serializers.IntegerField()
    categories = CategoryDetailSerializer(
        source="category_set", read_only=True, many=True
    )
    price = serializers.DecimalField(
        max_digits=18, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        read_only_fields = ["name", "description", "price", "categories"]
        exclude = ["retired"]


class OrderLineSerializer(serializers.ModelSerializer):
    product = ProductSerializerReadOnly()
    quantity = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(MAXNUMBERSIZE)],
    )
    subTotal = serializers.DecimalField(
        source="sub_total",
        read_only=True,
        decimal_places=2,
        max_digits=18,
    )

    class Meta:
        model = OrderLine
        fields = ["product", "quantity", "subTotal"]
        depth = 2


class OrderSerializer(serializers.ModelSerializer):
    createdOn = serializers.DateTimeField(source="created_on", read_only=True)
    lastUpdated = serializers.DateTimeField(
        source="last_updated", read_only=True
    )
    orderStatus = serializers.CharField(source="order_status", read_only=True)
    orderTotal = serializers.DecimalField(
        source="order_total",
        read_only=True,
        decimal_places=2,
        max_digits=18,
    )
    lineItems = OrderLineSerializer(
        source="orderline_set", many=True, required=False
    )

    def create(self, validated_data: dict) -> Order:
        order: Order = Order.objects.create()
        if "orderline_set" in validated_data:
            line_items_data: list[OrderedDict] = validated_data[
                "orderline_set"
            ]
            self.create_and_add_products_to_order(
                order=order, line_items_data=line_items_data
            )
        order.calculate_total()
        return order

    def update(self, order_to_update: Order, validated_data: dict) -> Order:
        if "orderline_set" in validated_data:
            line_items_data: list[OrderedDict] = validated_data[
                "orderline_set"
            ]
            self.check_products(line_items_data)
            OrderLine.objects.filter(order_id=order_to_update.id).delete()
            self.create_and_add_products_to_order(
                order=order_to_update, line_items_data=line_items_data
            )
        else:
            OrderLine.objects.filter(order_id=order_to_update.id).delete()
        order_to_update.calculate_total()

        return order_to_update

    def check_products(self, line_items_data: list[OrderedDict]):
        for order_item in line_items_data:
            get_object_or_400(Product, pk=order_item["product"]["id"])

    def create_and_add_products_to_order(
        self, order: Order, line_items_data: list[OrderedDict]
    ):
        for order_item in line_items_data:
            product: Product = Product.objects.get(
                pk=order_item["product"]["id"]
            )
            if product.retired or order_item["quantity"] < 1:
                continue
            new_line_item = OrderLine.objects.create(
                order=order, product=product, quantity=order_item["quantity"]
            )
            new_line_item.calculate_sub_total()

    class Meta:
        model = Order
        fields = (
            "id",
            "createdOn",
            "lastUpdated",
            "orderStatus",
            "orderTotal",
            "lineItems",
        )
        depth = 3
