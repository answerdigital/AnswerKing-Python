from decimal import Decimal

from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Product
from answerking_app.models.serializers import ProductSerializerReadOnly
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
        cat.products.add(prod)


    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()

    def test_product_read_only_serializer_contains_correct_fields(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializerReadOnly(test_prod).data
        expected: list[str] = [
            "id",
            "name",
            "description",
            "price",
            "categories",
        ]
        actual: list[str] = list(test_serializer_data.keys())
        self.assertCountEqual(actual, expected)

    def test_product_read_only_serializer_id_field_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializerReadOnly(test_prod).data
        expected: int = test_prod.id
        actual: int = test_serializer_data["id"]
        self.assertEqual(actual, expected)

    def test_product_read_only_serializer_name_field_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializerReadOnly(test_prod).data
        expected: str = test_prod.name
        actual: str = test_serializer_data["name"]
        self.assertEqual(actual, expected)

    def test_product_read_only_serializer_name_description_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializerReadOnly(test_prod).data
        expected: str = test_prod.description
        actual: str = test_serializer_data["description"]
        self.assertEqual(actual, expected)

    def test_product_read_only_serializer_name_price_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializerReadOnly(test_prod).data
        expected: Decimal = test_prod.price
        actual: Decimal = test_serializer_data["price"]
        self.assertEqual(actual, expected)

    def test_product_read_only_serializer_name_categories_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        category = test_prod.category_set.first()
        test_serializer_data: ReturnDict = ProductSerializerReadOnly(test_prod).data
        actual_category = test_serializer_data["categories"][0]

        self.assertEqual(actual_category["id"], category.id)
        self.assertEqual(actual_category["name"], category.name)
        self.assertEqual(actual_category["description"], category.description)

    def test_product_read_only_serializer_price_max_length_fail(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_prod.price = "1" * 19
        serializer = ProductSerializerReadOnly(data=test_prod)

        self.assertFalse(serializer.is_valid())

    def test_product_read_only_serializer_price_decimal_fail(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_prod.price = "1.111"
        serializer = ProductSerializerReadOnly(data=test_prod)

        self.assertFalse(serializer.is_valid())

    def test_product_read_only_serializer_price_negative_number_fail(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_prod.price = "-1"
        serializer = ProductSerializerReadOnly(data=test_prod)

        self.assertFalse(serializer.is_valid())
