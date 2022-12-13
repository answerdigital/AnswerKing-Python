from decimal import Decimal
from typing import OrderedDict
from unittest import mock

from django.db.models import QuerySet
from freezegun import freeze_time
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Order, Product, LineItem
from answerking_app.models.serializers import OrderSerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class OrderSerializerUnitTests(UnitTestBase):
    UBT = UnitTestBase()
    serializer_path: str = "answerking_app.models.serializers."
    test_prod_1_data: dict = UBT.get_fixture(
        "products", "plain_burger_data.json"
    )
    test_prod_2_data: dict = UBT.get_fixture(
        "products", "margarita_pizza_data.json"
    )
    test_order_1_data: dict = UBT.get_fixture("orders", "order_data.json")
    test_order_2_data: dict = UBT.get_fixture("orders", "order_data_2.json")

    frozen_time: str = "2022-01-01T01:02:03.000000Z"
    frozen_time_update: str = "2022-07-01T01:32:03.000000Z"

    @freeze_time(frozen_time)
    def setUp(self):
        valid_order: Order = Order.objects.create()
        product_burger: Product = Product.objects.create(
            **self.test_prod_1_data
        )
        self.test_order_1_data["lineItems"][0]["product"][
            "id"
        ] = product_burger.id
        product_pizza: Product = Product.objects.create(
            **self.test_prod_2_data
        )
        self.test_order_2_data["lineItems"][0]["product"][
            "id"
        ] = product_pizza.id

        line_item = LineItem.objects.create(
            order=valid_order, product=product_burger, quantity=3
        )
        line_item.calculate_sub_total()
        valid_order.calculate_total()

    def tearDown(self):
        Order.objects.all().delete()
        Product.objects.all().delete()
        LineItem.objects.all().delete()

    def test_order_serializer_contains_correct_fields(self):
        orders: QuerySet[Order] = Order.objects.all()
        order: Order = orders.first()
        test_serializer_data: ReturnDict = OrderSerializer(order).data
        expected: list[str] = [
            "id",
            "createdOn",
            "lastUpdated",
            "orderStatus",
            "orderTotal",
            "lineItems",
        ]
        actual: list[str] = list(test_serializer_data.keys())
        self.assertEqual(actual, expected)
        self.assertEqual(orders.count(), 1)

    def test_order_serializer_id_field_content(self):
        orders: QuerySet[Order] = Order.objects.all()
        order: Order = orders.first()
        test_serializer_data: ReturnDict = OrderSerializer(order).data
        expected: int = order.id
        actual: int = test_serializer_data["id"]
        self.assertEqual(actual, expected)
        self.assertEqual(orders.count(), 1)

    def test_order_serializer_products_details_content(self):
        orders: QuerySet[Order] = Order.objects.all()
        order: Order = orders.first()
        test_serializer_data: ReturnDict = OrderSerializer(order).data[
            "lineItems"
        ][0]

        expected_product_id: dict = order.lineitem_set.values("product_id")[0]
        actual_product_id: dict = {
            "product_id": test_serializer_data["product"]["id"]
        }

        expected_quantity: dict = order.lineitem_set.values("quantity")[0]
        actual_quantity: dict = {"quantity": test_serializer_data["quantity"]}

        expected_product_subtotal: dict = order.lineitem_set.values(
            "sub_total"
        )[0]
        actual_product_subtotal: dict = {
            "sub_total": test_serializer_data["subTotal"]
        }

        self.assertEqual(actual_product_id, expected_product_id)
        self.assertEqual(actual_quantity, expected_quantity)
        self.assertEqual(actual_product_subtotal, expected_product_subtotal)
        self.assertEqual(orders.count(), 1)
        self.assertEqual(order.lineitem_set.count(), 1)

    def test_order_serializer_order_status_field_content(self):
        orders: QuerySet[Order] = Order.objects.all()
        order: Order = orders.first()
        test_serializer_data: ReturnDict = OrderSerializer(order).data
        expected_status: str = order.order_status
        actual_status: str = test_serializer_data["orderStatus"]
        self.assertEqual(actual_status, expected_status)
        self.assertEqual(orders.count(), 1)

    def test_order_serializer_order_total_field_content(self):
        orders: QuerySet[Order] = Order.objects.all()
        order: Order = orders.first()
        test_serializer_data: ReturnDict = OrderSerializer(order).data
        expected_total: Decimal = order.order_total
        actual_total: Decimal = test_serializer_data["orderTotal"]
        self.assertEqual(actual_total, expected_total)
        self.assertEqual(orders.count(), 1)

    @freeze_time(frozen_time)
    def test_order_serializer_created_on_and_last_updated_field_content(self):
        orders: QuerySet[Order] = Order.objects.all()
        order: Order = orders.first()
        test_serializer_data: ReturnDict = OrderSerializer(order).data
        expected: str = self.frozen_time
        actual_created: str = test_serializer_data["createdOn"]
        actual_updated: str = test_serializer_data["lastUpdated"]
        self.assertEqual(actual_created, expected)
        self.assertEqual(actual_updated, expected)
        self.assertEqual(orders.count(), 1)

    @freeze_time(frozen_time)
    @mock.patch(
        serializer_path + "OrderSerializer.products_check",
        return_value=[],
    )
    def test_valid_order_create(self, products_check_mock):
        new_order_data = OrderSerializer(data=self.test_order_1_data)
        new_order_data.is_valid()
        serializer = OrderSerializer()
        new_order_object = serializer.create(new_order_data.validated_data)
        new_order_serializer_data: ReturnDict = OrderSerializer(
            new_order_object
        ).data
        test_json_data = self.test_order_1_data["lineItems"][0]

        expected_product_id: dict = new_order_object.lineitem_set.values(
            "product_id"
        )[0]
        actual_product_id: dict = {
            "product_id": test_json_data["product"]["id"]
        }

        expected_quantity: dict = new_order_object.lineitem_set.values(
            "quantity"
        )[0]
        actual_quantity: dict = {"quantity": test_json_data["quantity"]}

        expected_time: str = self.frozen_time
        actual_created: str = new_order_serializer_data["createdOn"]
        actual_updated: str = new_order_serializer_data["lastUpdated"]

        expected_status: str = "Created"
        actual_status: str = new_order_object.order_status

        expected_total: Decimal = Decimal(60.00)
        actual_total: Decimal = new_order_object.order_total
        products_check_mock.assert_called_once()

        self.assertEqual(actual_total, expected_total)
        self.assertEqual(actual_product_id, expected_product_id)
        self.assertEqual(actual_total, expected_total)
        self.assertEqual(actual_quantity, expected_quantity)
        self.assertEqual(actual_created, expected_time)
        self.assertEqual(actual_updated, expected_time)
        self.assertEqual(actual_status, expected_status)

    @freeze_time(frozen_time)
    @mock.patch(
        serializer_path + "OrderSerializer.products_check",
        return_value=[],
    )
    def test_empty_order_create(self, products_check_mock):
        serializer = OrderSerializer()
        new_order_object = serializer.create(validated_data={})
        new_order_serializer_data: ReturnDict = OrderSerializer(
            new_order_object
        ).data
        expected_fields: list[str] = [
            "id",
            "createdOn",
            "lastUpdated",
            "orderStatus",
            "orderTotal",
            "lineItems",
        ]
        actual_fields: list[str] = list(new_order_serializer_data.keys())

        expected_time: str = self.frozen_time
        actual_created: str = new_order_serializer_data["createdOn"]
        actual_updated: str = new_order_serializer_data["lastUpdated"]

        expected_status: str = "Created"
        actual_status: str = new_order_object.order_status

        expected_total: Decimal = Decimal(0.00)
        actual_total: Decimal = new_order_object.order_total

        products_check_mock.assert_not_called()
        self.assertEqual(actual_total, expected_total)
        self.assertEqual(actual_created, expected_time)
        self.assertEqual(actual_updated, expected_time)
        self.assertEqual(actual_status, expected_status)
        self.assertEqual(actual_fields, expected_fields)
        self.assertEqual(
            new_order_serializer_data["lineItems"],
            list(new_order_object.lineitem_set.values()),
        )

    @freeze_time(frozen_time)
    @mock.patch(
        serializer_path + "OrderSerializer.products_check",
        return_value=[],
    )
    def test_order_create_with_retired_product(self, products_check_mock):
        existing_product: Product = Product.objects.get(name="Plain Burger")
        existing_product.retired = True
        existing_product.save()
        new_order_data = OrderSerializer(data=self.test_order_1_data)
        new_order_data.is_valid()
        serializer = OrderSerializer()
        new_order_object = serializer.create(new_order_data.validated_data)
        new_order_serializer_data: ReturnDict = OrderSerializer(
            new_order_object
        ).data

        expected_time: str = self.frozen_time
        actual_created: str = new_order_serializer_data["createdOn"]
        actual_updated: str = new_order_serializer_data["lastUpdated"]

        expected_status: str = "Created"
        actual_status: str = new_order_object.order_status

        expected_total: Decimal = Decimal(0.00)
        actual_total: Decimal = new_order_object.order_total

        products_check_mock.assert_called_once()
        new_line_item = LineItem.objects.filter(
            order=new_order_object, product=existing_product
        )

        self.assertEqual(new_line_item.count(), 0)
        self.assertEqual(actual_total, expected_total)
        self.assertEqual(actual_created, expected_time)
        self.assertEqual(actual_updated, expected_time)
        self.assertEqual(actual_status, expected_status)

    @freeze_time(frozen_time_update)
    @mock.patch(
        serializer_path + "OrderSerializer.products_check",
        return_value=[],
    )
    def test_valid_order_update(self, products_check_mock):
        orders: QuerySet[Order] = Order.objects.all()
        old_order: Order = orders.first()
        updated_order_data = OrderSerializer(data=self.test_order_2_data)
        updated_order_data.is_valid()
        serializer = OrderSerializer()
        new_order_object = serializer.update(
            old_order, updated_order_data.validated_data
        )
        new_order_serializer_data: ReturnDict = OrderSerializer(
            new_order_object
        ).data
        test_json_data = self.test_order_2_data["lineItems"][0]

        expected_product_id: dict = new_order_object.lineitem_set.values(
            "product_id"
        )[0]
        actual_product_id: dict = {
            "product_id": test_json_data["product"]["id"]
        }

        expected_quantity: dict = new_order_object.lineitem_set.values(
            "quantity"
        )[0]
        actual_quantity: dict = {"quantity": test_json_data["quantity"]}

        expected_create_time: str = self.frozen_time
        actual_created: str = new_order_serializer_data["createdOn"]

        expected_update_time: str = self.frozen_time_update
        actual_updated: str = new_order_serializer_data["lastUpdated"]

        expected_status: str = "Created"
        actual_status: str = new_order_object.order_status

        expected_total: Decimal = Decimal(42.00)
        actual_total: Decimal = new_order_object.order_total

        products_check_mock.assert_called_once()
        self.assertEqual(new_order_object.lineitem_set.count(), 1)
        self.assertEqual(actual_product_id, expected_product_id)
        self.assertEqual(actual_total, expected_total)
        self.assertEqual(actual_quantity, expected_quantity)
        self.assertEqual(actual_created, expected_create_time)
        self.assertEqual(actual_updated, expected_update_time)
        self.assertEqual(actual_status, expected_status)
        self.assertEqual(orders.count(), 1)

    @freeze_time(frozen_time_update)
    @mock.patch(
        serializer_path + "OrderSerializer.products_check",
        return_value=[],
    )
    def test_valid_order_update_with_empty_order(self, products_check_mock):
        orders: QuerySet[Order] = Order.objects.all()
        old_order: Order = orders.first()
        serializer = OrderSerializer()
        new_order_object = serializer.update(old_order, {})
        new_order_serializer_data: ReturnDict = OrderSerializer(
            new_order_object
        ).data

        expected_create_time: str = self.frozen_time
        actual_created: str = new_order_serializer_data["createdOn"]

        expected_update_time: str = self.frozen_time_update
        actual_updated: str = new_order_serializer_data["lastUpdated"]

        expected_status: str = "Created"
        actual_status: str = new_order_object.order_status

        expected_total: Decimal = Decimal(0.00)
        actual_total: Decimal = new_order_object.order_total

        products_check_mock.assert_not_called()
        self.assertEqual(new_order_object.lineitem_set.count(), 0)
        self.assertEqual(actual_total, expected_total)
        self.assertEqual(actual_created, expected_create_time)
        self.assertEqual(actual_updated, expected_update_time)
        self.assertEqual(actual_status, expected_status)
        self.assertEqual(orders.count(), 1)

    @freeze_time(frozen_time_update)
    @mock.patch(
        serializer_path + "OrderSerializer.products_check",
        return_value=[],
    )
    def test_empty_order_update_with_product(self, products_check_mock):
        empty_order: Order = Order.objects.create()
        updated_order_data = OrderSerializer(data=self.test_order_2_data)
        updated_order_data.is_valid()
        serializer = OrderSerializer()
        new_order_object = serializer.update(
            empty_order, updated_order_data.validated_data
        )
        new_order_serializer_data: ReturnDict = OrderSerializer(
            new_order_object
        ).data
        test_json_data = self.test_order_2_data["lineItems"][0]

        expected_product_id: dict = new_order_object.lineitem_set.values(
            "product_id"
        )[0]
        actual_product_id: dict = {
            "product_id": test_json_data["product"]["id"]
        }

        expected_quantity: dict = new_order_object.lineitem_set.values(
            "quantity"
        )[0]
        actual_quantity: dict = {"quantity": test_json_data["quantity"]}

        expected_create_time: str = self.frozen_time_update
        actual_created: str = new_order_serializer_data["createdOn"]

        expected_update_time: str = self.frozen_time_update
        actual_updated: str = new_order_serializer_data["lastUpdated"]

        expected_status: str = "Created"
        actual_status: str = new_order_object.order_status

        expected_total: Decimal = Decimal(42.00)
        actual_total: Decimal = new_order_object.order_total

        products_check_mock.assert_called_once()
        self.assertEqual(new_order_object.lineitem_set.count(), 1)
        self.assertEqual(actual_product_id, expected_product_id)
        self.assertEqual(actual_total, expected_total)
        self.assertEqual(actual_quantity, expected_quantity)
        self.assertEqual(actual_created, expected_create_time)
        self.assertEqual(actual_updated, expected_update_time)
        self.assertEqual(actual_status, expected_status)

    @freeze_time(frozen_time)
    @mock.patch(
        serializer_path + "OrderSerializer.products_check",
        return_value=[],
    )
    def test_order_update_with_retired_product(self, products_check_mock):
        orders: QuerySet[Order] = Order.objects.all()
        old_order: Order = orders.first()
        existing_product: Product = Product.objects.get(name="Margarita pizza")
        existing_product.retired = True
        existing_product.save()
        new_order_data = OrderSerializer(data=self.test_order_2_data)
        new_order_data.is_valid()
        serializer = OrderSerializer()
        new_order_object = serializer.update(
            old_order, new_order_data.validated_data
        )
        new_order_serializer_data: ReturnDict = OrderSerializer(
            new_order_object
        ).data

        expected_time: str = self.frozen_time
        actual_created: str = new_order_serializer_data["createdOn"]
        actual_updated: str = new_order_serializer_data["lastUpdated"]

        expected_status: str = "Created"
        actual_status: str = new_order_object.order_status

        expected_total: Decimal = Decimal(0.00)
        actual_total: Decimal = new_order_object.order_total

        products_check_mock.assert_called_once()
        new_line_item = LineItem.objects.filter(
            order=new_order_object, product=existing_product
        )

        self.assertEqual(new_line_item.count(), 0)
        self.assertEqual(actual_total, expected_total)
        self.assertEqual(actual_created, expected_time)
        self.assertEqual(actual_updated, expected_time)
        self.assertEqual(actual_status, expected_status)
        self.assertEqual(orders.count(), 1)

    def test_create_order_line_items(self):
        orders: QuerySet[Order] = Order.objects.all()
        existing_order: Order = orders.first()
        existing_product: Product = Product.objects.get(name="Margarita pizza")
        serializer = OrderSerializer()
        updated_order_data = OrderSerializer(data=self.test_order_2_data)
        updated_order_data.is_valid()
        line_items_data: list[OrderedDict] = updated_order_data.validated_data[
            "lineitem_set"
        ]
        serializer.create_order_line_items(existing_order, line_items_data)

        new_line_item = LineItem.objects.get(
            order=existing_order, product=existing_product
        )

        expected_quantity: dict = self.test_order_2_data["lineItems"][0][
            "quantity"
        ]
        actual_quantity: dict = new_line_item.quantity

        expected_sub_total: Decimal = Decimal(42.00)
        actual_sub_total: Decimal = new_line_item.sub_total

        self.assertIsNotNone(new_line_item)
        self.assertEqual(expected_quantity, actual_quantity)
        self.assertEqual(expected_sub_total, actual_sub_total)
        self.assertEqual(orders.count(), 1)

    def test_create_order_line_items_with_retired_product(self):
        orders: QuerySet[Order] = Order.objects.all()
        existing_order: Order = orders.first()
        existing_product: Product = Product.objects.get(name="Margarita pizza")
        existing_product.retired = True
        existing_product.save()
        serializer = OrderSerializer()
        updated_order_data = OrderSerializer(data=self.test_order_2_data)
        updated_order_data.is_valid()
        line_items_data: list[OrderedDict] = updated_order_data.validated_data[
            "lineitem_set"
        ]
        serializer.create_order_line_items(existing_order, line_items_data)

        new_line_item = LineItem.objects.filter(
            order=existing_order, product=existing_product
        )
        self.assertEqual(new_line_item.count(), 0)
        self.assertEqual(orders.count(), 1)
