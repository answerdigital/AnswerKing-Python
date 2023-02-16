import copy
from decimal import Decimal

from rest_framework import serializers

from answerking_app.models.models import LineItem, Order, Product
from answerking_app.models.serializers import LineItemSerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class LineItemSerializerUnitTests(UnitTestBase):
    UTB = UnitTestBase()
    prod_data: dict = UTB.get_fixture("products", "plain_burger_data.json")
    quant: int = 3

    serialized_product_detail = copy.deepcopy(prod_data)
    serialized_product_detail["id"] = 1
    serialized_product_detail["category"] = []
    del serialized_product_detail["retired"]

    @staticmethod
    def serializer_is_valid(serializer: serializers.ModelSerializer) -> bool:
        valid = False
        if serializer.is_valid():
            valid = True
        return valid

    def setUp(self):
        self.prod: Product = Product.objects.create(**self.prod_data)
        order: Order = Order.objects.create()
        line_item: LineItem = LineItem.objects.create(
            order=order, product=self.prod, quantity=self.quant
        )
        line_item.calculate_sub_total()

    def tearDown(self):
        Product.objects.all().delete()
        Order.objects.all().delete()

    def test_line_item_serializer_contains_correct_fields(self):
        test_order: Order = Order.objects.all()[0]
        test_line_item: LineItem = test_order.lineitem_set.get(
            order=test_order
        )
        test_serializer_data: dict = LineItemSerializer(test_line_item).data
        expected: list[str] = ["product", "quantity", "subTotal"]
        actual: list[str] = list(test_serializer_data.keys())
        self.assertCountEqual(expected, actual)

    def test_line_item_serializer_product_content(self):
        test_order: Order = Order.objects.all()[0]
        test_line_item: LineItem = test_order.lineitem_set.get(
            order=test_order
        )
        test_serializer_data: dict = LineItemSerializer(test_line_item).data
        expected: Product = Product.objects.all()[0]
        actual = dict(**test_serializer_data["product"])
        self.assertEqual(expected.name, actual["name"])
        self.assertEqual(expected.description, actual["description"])
        self.assertEqual(expected.price, actual["price"])

    def test_line_item_serializer_quantity_content(self):
        test_order: Order = Order.objects.all()[0]
        test_line_item: LineItem = test_order.lineitem_set.get(
            order=test_order
        )
        test_serializer_data: dict = LineItemSerializer(test_line_item).data
        expected: int = self.quant
        actual: int = test_serializer_data["quantity"]
        self.assertEqual(expected, actual)

    def test_line_item_serializer_quantity_less_than_zero_fail(self):
        serializer_data = {
            "productId": self.prod.id,
            "quantity": -1,
        }
        serializer = LineItemSerializer(data=serializer_data)
        valid = self.serializer_is_valid(serializer)

        self.assertEqual(valid, False)
        self.assertEqual(len(serializer.errors), 1)
        self.assertIn("quantity", serializer.errors.keys())
        self.assertEqual(
            "Ensure this value is greater than or equal to 0.",
            serializer.errors["quantity"][0],
        )

    def test_line_item_serializer_quantity_greater_than_max_val_fail(self):
        MAXNUMBERSIZE: int = 2147483647
        serializer_data = {
            "productId": self.prod.id,
            "quantity": MAXNUMBERSIZE + 1,
        }
        serializer = LineItemSerializer(data=serializer_data)
        valid = self.serializer_is_valid(serializer)

        self.assertEqual(valid, False)
        self.assertEqual(len(serializer.errors), 1)
        self.assertIn("quantity", serializer.errors.keys())
        self.assertEqual(
            f"Ensure this value is less than or equal to {MAXNUMBERSIZE}.",
            serializer.errors["quantity"][0],
        )

    def test_line_item_serializer_sub_total_content(self):
        test_order = Order.objects.all()[0]
        test_line_item = test_order.lineitem_set.get(order=test_order)
        test_serializer_data: dict = LineItemSerializer(test_line_item).data
        expected: Decimal = test_line_item.sub_total
        actual: Decimal = test_serializer_data["subTotal"]
        self.assertEqual(expected, actual)
