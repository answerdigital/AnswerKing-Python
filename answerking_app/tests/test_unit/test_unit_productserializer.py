from decimal import Decimal

from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.serializers import ProductSerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class ProductSerializerTests(UnitTestBase):

    utb = UnitTestBase()

    serializer_path: str = "answerking_app.models.serializers."
    test_product_serializer_data: dict[str | None] = utb.get_fixture(
        "products", "prod_with_id_data.json"
    )
    test_product_serializer: ProductSerializer = ProductSerializer(
        test_product_serializer_data
    )

    def test_product_serializer_contains_correct_fields(self):
        data: ReturnDict = self.test_product_serializer.instance
        self.assertCountEqual(
            data.keys(),
            [
                "id",
                "name",
                "description",
                "price",
                "categories",
                "retired",
            ],
        )

    def test_product_serializer_id_field_content(self):
        data: ReturnDict = self.test_product_serializer.data
        expected: int = self.test_product_serializer_data["id"]
        actual: int = data["id"]
        self.assertEqual(actual, expected)

    def test_product_serializer_name_field_content(self):
        data: ReturnDict = self.test_product_serializer.data
        expected: str = self.test_product_serializer_data["name"]
        actual: str = data["name"]
        self.assertEqual(actual, expected)

    def test_product_serializer_description_field_content(self):
        data: ReturnDict = self.test_product_serializer.data
        expected: str = self.test_product_serializer_data["description"]
        actual: str = data["description"]
        self.assertEqual(actual, expected)

    def test_product_serializer_price_field_content(self):
        data: ReturnDict = self.test_product_serializer.data
        expected: Decimal = self.test_product_serializer_data["price"]
        actual: Decimal = data["price"]
        self.assertEqual(actual, expected)

    def test_product_serializer_categories_field_content(self):
        data: ReturnDict = self.test_product_serializer.instance
        self.assertEqual(
            data["categories"],
            self.test_product_serializer.instance["categories"],
        )

    def test_product_serializer_retired_field_content(self):
        data: ReturnDict = self.test_product_serializer.data
        expected: bool = self.test_product_serializer_data["retired"]
        actual: bool = data["retired"]
        self.assertEqual(actual, expected)

    def test_product_serializer_name_max_length_fail(self):
        serializer_data: dict = self.test_product_serializer.data
        serializer_data["name"] = "e" * 51
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_product_serializer_name_blank_fail(self):
        serializer_data: dict = self.test_product_serializer.data
        serializer_data["name"] = ""
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_product_serializer_name_regex_validator_pass_1(self):
        allowed_characters: str = "abcdefghijklm nopqrstuvwxyz"
        serializer_data = self.test_product_serializer.data
        serializer_data["name"] = allowed_characters
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], allowed_characters)

    def test_product_serializer_name_regex_validator_pass_2(self):
        allowed_characters: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!"
        serializer_data = self.test_product_serializer.data
        serializer_data["name"] = allowed_characters
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], allowed_characters)

    def test_product_serializer_name_regex_validator_fail(self):
        allowed_characters: str = "abcdefghijklmnopqrstuvwxyz "
        serializer_data = self.test_product_serializer.data
        serializer_data["name"] = allowed_characters + "#"
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_product_serializer_price_max_length_fail(self):
        serializer_data = self.test_product_serializer.data
        serializer_data["price"] = "1" * 19
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"price"})

    def test_product_serializer_price_decimal_fail(self):
        serializer_data = self.test_product_serializer.data
        serializer_data["price"] = "1.111"
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"price"})

    def test_product_serializer_price_negative_number_fail(self):
        serializer_data = self.test_product_serializer.data
        serializer_data["price"] = "-1"
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"price"})

    def test_product_serializer_desc_max_length_fail(self):
        serializer_data = self.test_product_serializer.data
        serializer_data["description"] = "e" * 201
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"description"})

    def test_product_serializer_desc_blank_pass(self):
        serializer_data = self.test_product_serializer.data
        serializer_data["description"] = ""
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["description"], "")

    def test_product_serializer_desc_regex_validator_pass_1(self):
        allowed_characters: str = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,# .!"
        )
        serializer_data = self.test_product_serializer.data
        serializer_data["description"] = allowed_characters
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["description"], allowed_characters)

    def test_product_serializer_desc_regex_validator_fail(self):
        allowed_characters: str = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,# .!"
        )
        serializer_data = self.test_product_serializer.data
        serializer_data["description"] = allowed_characters + "*"
        serializer: ProductSerializer = ProductSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"description"})
