from decimal import Decimal
import copy

from django.db.models import QuerySet
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Product
from answerking_app.models.serializers import ProductSerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class ProductSerializerTests(UnitTestBase):

    utb = UnitTestBase()

    serializer_path: str = "answerking_app.models.serializers."
    test_cat_data: dict = utb.get_fixture(
        "categories", "burgers_cat_data.json"
    )
    test_prod_data: dict = utb.get_fixture(
        "products", "plain_burger_data.json"
    )

    def setUp(self):
        cat: Category = Category.objects.create(**self.test_cat_data)
        prod: Product = Product.objects.create(**self.test_prod_data)
        cat.products.add(prod)

    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()

    def test_product_serializer_contains_correct_fields(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializer(test_prod).data
        expected: list[str] = [
            "id",
            "name",
            "description",
            "price",
            "categories",
            "retired",
        ]
        actual: list[str] = list(test_serializer_data.keys())
        self.assertEqual(actual, expected)

    def test_product_serializer_id_field_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializer(test_prod).data
        expected: int = test_prod.id
        actual: int = test_serializer_data["id"]
        self.assertEqual(actual, expected)

    def test_product_serializer_name_field_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializer(test_prod).data
        expected: str = test_prod.name
        actual: str = test_serializer_data["name"]
        self.assertEqual(actual, expected)

    def test_product_serializer_description_field_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializer(test_prod).data
        expected: str = test_prod.description
        actual: str = test_serializer_data["description"]
        self.assertEqual(actual, expected)

    def test_product_serializer_price_field_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializer(test_prod).data
        expected: Decimal = test_prod.price
        actual: Decimal = test_serializer_data["price"]
        self.assertEqual(actual, expected)

    def test_product_serializer_categories_field_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        categories: QuerySet[Category] = test_prod.category_set.all()
        category: Category = categories[0]
        test_serializer_data: ReturnDict = ProductSerializer(test_prod).data
        actual_category: dict = test_serializer_data["categories"][0]

        self.assertEqual(len(categories), 1)
        self.assertEqual(actual_category["id"], category.id)
        self.assertEqual(actual_category["name"], category.name)
        self.assertEqual(actual_category["description"], category.description)

    def test_product_serializer_retired_field_content(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        test_serializer_data: ReturnDict = ProductSerializer(test_prod).data
        expected: bool = test_prod.retired
        actual: bool = test_serializer_data["retired"]
        self.assertEqual(actual, expected)

    def test_product_serializer_name_max_length_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        serializer_data["name"] = "e" * 51
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_product_serializer_name_blank_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        serializer_data["name"] = ""
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_product_serializer_name_regex_validator_pass_1(self):
        allowed_characters: str = "abcdefghijklm nopqrstuvwxyz"
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        serializer_data["name"] = allowed_characters
        serializer = ProductSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], allowed_characters)

    def test_product_serializer_name_regex_validator_pass_2(self):
        allowed_characters: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!"
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        serializer_data["name"] = allowed_characters
        serializer = ProductSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], allowed_characters)

    def test_product_serializer_name_regex_validator_fail(self):
        allowed_characters: str = "abcdefghijklmnopqrstuvwxyz "
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        serializer_data["name"] = allowed_characters + "#"
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_product_serializer_price_max_value_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        max_number_size: int = 2147483647
        serializer_data["price"] = max_number_size + 1
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"price"})

    def test_product_serializer_price_decimal_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        serializer_data["price"] = "1.111"
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"price"})

    def test_product_serializer_desc_max_length_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        serializer_data["description"] = "e" * 201
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"description"})

    def test_product_serializer_desc_blank_pass(self):
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        serializer_data["description"] = ""
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["description"], "")

    def test_product_serializer_desc_regex_validator_pass_1(self):
        allowed_characters: str = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,# .!"
        )
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        serializer_data["description"] = allowed_characters
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["description"], allowed_characters)

    def test_product_serializer_desc_regex_validator_fail(self):
        allowed_characters: str = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,# .!"
        )
        serializer_data: dict = copy.deepcopy(self.test_prod_data)
        serializer_data["description"] = allowed_characters + "*"
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"description"})
