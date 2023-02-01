from decimal import Decimal

from django.db.models import QuerySet
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Product
from answerking_app.models.serializers import LineItemProductSerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class ProductSerializerTests(UnitTestBase):
    UTB = UnitTestBase()
    test_cat_data: dict = UTB.get_fixture(
        "categories", "burgers_cat_data.json"
    )
    test_prod_data: dict = UTB.get_fixture(
        "products", "plain_burger_data.json"
    )

    def setUp(self):
        cat: Category = Category.objects.create(**self.test_cat_data)
        prod: Product = Product.objects.create(**self.test_prod_data)
        cat.product_set.add(prod)

    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()

    def test_product_read_only_serializer_contains_correct_fields(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = LineItemProductSerializer(
            test_prod
        ).data
        expected: list[str] = [
            "id",
            "price",
            "name",
            "description",
        ]
        actual: list[str] = list(test_serializer_data.keys())
        self.assertEqual(actual, expected)

    def test_product_read_only_serializer_id_field_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = LineItemProductSerializer(
            test_prod
        ).data
        expected: int = test_prod.id
        actual: int = test_serializer_data["id"]
        self.assertEqual(actual, expected)

    def test_product_read_only_serializer_name_field_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = LineItemProductSerializer(
            test_prod
        ).data
        expected: str = test_prod.name
        actual: str = test_serializer_data["name"]
        self.assertEqual(actual, expected)

    def test_product_read_only_serializer_description_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = LineItemProductSerializer(
            test_prod
        ).data
        expected: str = test_prod.description
        actual: str = test_serializer_data["description"]
        self.assertEqual(actual, expected)

    def test_product_read_only_serializer_price_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = LineItemProductSerializer(
            test_prod
        ).data
        expected: Decimal = test_prod.price
        actual: Decimal = test_serializer_data["price"]
        self.assertEqual(actual, expected)

    def test_product_read_only_serializer_price_max_value_fail(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        max_number_size: int = 2147483647
        test_prod.price = max_number_size + 1
        serializer: LineItemProductSerializer = LineItemProductSerializer(
            data=test_prod
        )

        self.assertFalse(serializer.is_valid())

    def test_product_read_only_serializer_price_decimal_fail(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_prod.price = "1.111"
        serializer: LineItemProductSerializer = LineItemProductSerializer(
            data=test_prod
        )

        self.assertFalse(serializer.is_valid())
