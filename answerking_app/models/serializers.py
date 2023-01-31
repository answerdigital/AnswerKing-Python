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
    LineItem,
)
from answerking_app.utils.serializer_data_functions import (
    products_check,
    compress_white_spaces,
)
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails

MAXNUMBERSIZE = 2147483647


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
        products: list[Product] = products_check(validated_data)
        category: Category = Category.objects.create(
            name=validated_data["name"],
            description=validated_data["description"],
        )
        category.product_set.add(*products)
        return category

    def update(self, category: Category, validated_data: dict) -> Category:
        if category.retired:
            raise ProblemDetails(
                status=status.HTTP_410_GONE,
                detail="This category has been retired",
            )
        products: list[Product] = products_check(validated_data)
        category.name = validated_data["name"]
        category.description = validated_data["description"]
        category.save()
        category.product_set.set(objs=products)
        return category

    class Meta:
        model = Category
        fields = ("id", "name", "description")

    def validate_name(self, value: str) -> str:
        return compress_white_spaces(value)


class CategorySerializer(CategoryDetailSerializer):
    createdOn = serializers.DateTimeField(source="created_on", read_only=True)
    lastUpdated = serializers.DateTimeField(
        source="last_updated", read_only=True
    )

    retired = serializers.BooleanField(required=False)
    products = serializers.PrimaryKeyRelatedField(
        source="product_set",
        many=True,
        queryset=Product.objects.all(),
        required=False,
    )

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


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        required=False, validators=[MinValueValidator(0)]
    )
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
    retired = serializers.BooleanField(required=False)
    category = CategoryDetailSerializer(read_only=True)
    categoryId = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Category.objects.all(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "category",
            "categoryId",
            "retired",
        )
        depth = 1

    def validate_name(self, value: str) -> str:
        return compress_white_spaces(value)

    def validate_description(self, value: str) -> str:
        return compress_white_spaces(value)


class LineItemProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    price = serializers.DecimalField(
        max_digits=18, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        read_only_fields = ["name", "description", "price"]
        exclude = ["retired", "category"]


class LineItemSerializer(serializers.ModelSerializer):
    product = LineItemProductSerializer()
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
        model = LineItem
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
    lineItems = LineItemSerializer(
        source="lineitem_set", many=True, required=False
    )

    def create(self, validated_data: dict) -> Order:
        order: Order = Order.objects.create()
        if "lineitem_set" in validated_data:
            line_items_data = validated_data["lineitem_set"]
            self.create_order_line_items(
                order=order, line_items_data=line_items_data
            )
        order.calculate_total()
        return order

    def update(self, order_to_update: Order, validated_data: dict) -> Order:
        if "lineitem_set" in validated_data:
            line_items_data: list[OrderedDict] = validated_data["lineitem_set"]
            LineItem.objects.filter(order_id=order_to_update.id).delete()
            self.create_order_line_items(
                order=order_to_update, line_items_data=line_items_data
            )
        else:
            LineItem.objects.filter(order_id=order_to_update.id).delete()
        order_to_update.calculate_total()

        return order_to_update

    def create_order_line_items(
        self,
        order: Order,
        line_items_data: list[OrderedDict],
    ):
        products_id_list = []
        for product in line_items_data:
            products_id_list.append(
                Product.objects.get(id=product["product"]["id"])
            )
        products = products_check({"product_set": products_id_list})
        for order_item, product in zip(line_items_data, products):
            if order_item["quantity"] < 1:
                continue
            new_line_item = LineItem.objects.create(
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


class ErrorDetailSerializer(serializers.Serializer):
    name = serializers.CharField()


class ProblemDetailSerializer(serializers.Serializer):
    errors = ErrorDetailSerializer(many=True)
    type = serializers.CharField()
    title = serializers.CharField()
    status = serializers.IntegerField()
    traceID = serializers.CharField()

    class Meta:
        fields = ("errors", "type", "title", "status", "traceID")
