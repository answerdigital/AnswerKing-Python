from decimal import Decimal

from freezegun import freeze_time
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Order, Product, LineItem
from answerking_app.models.serializers import OrderSerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class OrderSerializerUnitTests(UnitTestBase):
    UBT = UnitTestBase()
    serializer_path: str = "answerking_app.models.serializers."
    test_prod_data: dict = UBT.get_fixture(
        "products",
        "plain_burger_data.json"
    )
    test_order_data: dict = UBT.get_fixture(
        "orders",
        "order_data.json"
    )
    frozen_time: str = "2022-01-01T01:02:03.000000Z"

    @freeze_time(frozen_time)
    def setUp(self):
        order: Order = Order.objects.create()
        product: Product = Product.objects.create(**self.test_prod_data)
        line_item = LineItem.objects.create(order=order, product=product, quantity=3)
        line_item.calculate_sub_total()
        order.calculate_total()

    def tearDown(self):
        Order.objects.all().delete()
        Product.objects.all().delete()
        LineItem.objects.all().delete()

    def test_order_serializer_contains_correct_fields(self):
        order: Order = Order.objects.all().get()
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

    def test_order_serializer_id_field_content(self):
        order: Order = Order.objects.all().get()
        test_serializer_data: ReturnDict = OrderSerializer(order).data
        expected: int = order.id
        actual: int = test_serializer_data['id']
        self.assertEqual(actual, expected)

    def test_order_serializer_products_details_content(self):
        order: Order = Order.objects.all().get()
        test_serializer_data: ReturnDict = OrderSerializer(order).data["lineItems"][0]

        expected_product_id: dict = order.lineitem_set.values('product_id')[0]
        actual_product_id: dict = {'product_id': test_serializer_data['product']['id']}

        expected_quantity: dict = order.lineitem_set.values('quantity')[0]
        actual_quantity: dict = {'quantity': test_serializer_data['quantity']}

        expected_product_subtotal: dict = order.lineitem_set.values('sub_total')[0]
        actual_product_subtotal: dict = {'sub_total': test_serializer_data['subTotal']}

        self.assertEqual(actual_product_id, expected_product_id)
        self.assertEqual(actual_quantity, expected_quantity)
        self.assertEqual(actual_product_subtotal, expected_product_subtotal)

    def test_order_serializer_order_status_field_content(self):
        order: Order = Order.objects.all().get()
        test_serializer_data: ReturnDict = OrderSerializer(order).data
        expected_status: str = order.order_status
        actual_status: str = test_serializer_data["orderStatus"]
        self.assertEqual(actual_status, expected_status)

    def test_order_serializer_order_total_field_content(self):
        order: Order = Order.objects.all().get()
        test_serializer_data: ReturnDict = OrderSerializer(order).data
        expected_status: Decimal = order.order_total
        actual_status: Decimal = test_serializer_data["orderTotal"]
        self.assertEqual(actual_status, expected_status)

    @freeze_time(frozen_time)
    def test_order_serializer_created_on_and_last_updated_field_content(self):
        order: Order = Order.objects.all().get()
        test_serializer_data: ReturnDict = OrderSerializer(order).data
        expected: str = self.frozen_time
        actual_created: str = test_serializer_data["createdOn"]
        actual_updated: str = test_serializer_data["lastUpdated"]
        self.assertEqual(actual_created, expected)
        self.assertEqual(actual_updated, expected)

    def test_valid_order_create(self):
        new_order_data = OrderSerializer(data=self.test_order_data)
        new_order_data.is_valid()
        serializer = OrderSerializer()
        new_order_object = serializer.create(new_order_data.validated_data)
        test_serializer_data = self.test_order_data["lineItems"][0]

        expected_product_id: dict = new_order_object.lineitem_set.values('product_id')[0]
        actual_product_id: dict = {'product_id': test_serializer_data['product']['id']}

        expected_quantity: dict = new_order_object.lineitem_set.values('quantity')[0]
        actual_quantity: dict = {'quantity': test_serializer_data['quantity']}

        self.assertEqual(actual_product_id, expected_product_id)
        self.assertEqual(actual_quantity, expected_quantity)

    def test_empty_order_create(self):
        serializer = OrderSerializer()
        new_order_object = serializer.create(validated_data={})
        test_serializer_data: ReturnDict = OrderSerializer(new_order_object).data
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
        self.assertEqual(test_serializer_data['lineItems'], list(new_order_object.lineitem_set.values()))

    def test_valid_order_update(self):
        order: Order = Order.objects.all().get()
        updated_order_data = OrderSerializer(data=self.test_order_data)
        updated_order_data.is_valid()
        serializer = OrderSerializer()
        new_order_object = serializer.update(order, updated_order_data.validated_data)
        test_serializer_data = self.test_order_data["lineItems"][0]

        expected_product_id: dict = new_order_object.lineitem_set.values('product_id')[0]
        actual_product_id: dict = {'product_id': test_serializer_data['product']['id']}

        expected_quantity: dict = new_order_object.lineitem_set.values('quantity')[0]
        actual_quantity: dict = {'quantity': test_serializer_data['quantity']}

        self.assertEqual(actual_product_id, expected_product_id)
        self.assertEqual(actual_quantity, expected_quantity)
