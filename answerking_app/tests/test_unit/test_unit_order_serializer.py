from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Order, Product, LineItem
from answerking_app.models.serializers import OrderSerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class OrderSerializerUnitTests(UnitTestBase):
    UBT = UnitTestBase()

    test_prod_data: dict = UBT.get_fixture(
        "products",
        "plain_burger_data.json"
    )

    def setUp(self):
        order: Order = Order.objects.create()
        product: Product = Product.objects.create(**self.test_prod_data)
        line_item: LineItem = LineItem.objects.create(order=order, product=product, quantity=3)

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
        self.assertCountEqual(actual, expected)
