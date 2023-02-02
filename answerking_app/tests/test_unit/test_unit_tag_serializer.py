import copy

from django.db.models import QuerySet
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Tag, Product
from answerking_app.models.serializers import TagSerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class TagSerializerTests(UnitTestBase):
    utb = UnitTestBase()

    serializer_path: str = "answerking_app.models.serializers."
    test_tag_data: dict = utb.get_fixture("tags", "halal_tag_data.json")
    test_prod_data: dict = utb.get_fixture(
        "products", "plain_burger_data.json"
    )

    def setUp(self):
        tag: Tag = Tag.objects.create(**self.test_tag_data)
        prod: Product = Product.objects.create(**self.test_prod_data)
        tag.products.add(prod)

    def tearDown(self):
        Tag.objects.all().delete()
        Product.objects.all().delete()

    def test_tag_serializer_contains_correct_fields(self):
        test_tag: Tag = Tag.objects.get(name=self.test_tag_data["name"])
        test_serializer_data: ReturnDict = TagSerializer(test_tag).data
        expected: list[str] = [
            "id",
            "name",
            "description",
            "products",
            "retired",
        ]
        actual: list[str] = list(test_serializer_data.keys())
        self.assertEqual(actual, expected)

    def test_tag_serializer_id_field_content(self):
        test_tag: Tag = Tag.objects.get(name=self.test_tag_data["name"])
        test_serializer_data: ReturnDict = TagSerializer(test_tag).data
        expected: int = test_tag.id
        actual: int = test_serializer_data["id"]
        self.assertEqual(actual, expected)

    def test_tag_serializer_name_field_content(self):
        test_tag: Tag = Tag.objects.get(name=self.test_tag_data["name"])
        test_serializer_data: ReturnDict = TagSerializer(test_tag).data
        expected: str = test_tag.name
        actual: str = test_serializer_data["name"]
        self.assertEqual(actual, expected)

    def test_tag_serializer_description_field_content(self):
        test_tag: Tag = Tag.objects.get(name=self.test_tag_data["name"])
        test_serializer_data: ReturnDict = TagSerializer(test_tag).data
        expected: str = test_tag.description
        actual: str = test_serializer_data["description"]
        self.assertEqual(actual, expected)

    def test_tag_serializer_retired_field_content(self):
        test_tag: Tag = Tag.objects.get(name=self.test_tag_data["name"])
        test_serializer_data: ReturnDict = TagSerializer(test_tag).data
        expected: bool = test_tag.retired
        actual: bool = test_serializer_data["retired"]
        self.assertEqual(actual, expected)

    def test_tag_serializer_products_field_content(self):
        test_tag: Tag = Tag.objects.get(name=self.test_tag_data["name"])
        products: QuerySet[Product] = test_tag.products.all()
        product: Product = products[0]
        test_serializer_data: ReturnDict = TagSerializer(test_tag).data
        actual_product: int = test_serializer_data["products"][0]

        self.assertEqual(len(products), 1)
        self.assertEqual(actual_product, product.id)

    def test_tag_serializer_name_max_length_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_tag_data)
        serializer_data["name"] = "e" * 51
        serializer: TagSerializer = TagSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_tag_serializer_name_blank_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_tag_data)
        serializer_data["name"] = ""
        serializer: TagSerializer = TagSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_tag_serializer_name_regex_validator_pass_1(self):
        allowed_characters: str = "abcdefghijklm nopqrstuvwxyz"
        serializer_data: dict = copy.deepcopy(self.test_tag_data)
        serializer_data["name"] = allowed_characters
        serializer: TagSerializer = TagSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], allowed_characters)

    def test_tag_serializer_name_regex_validator_pass_2(self):
        allowed_characters: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!"
        serializer_data: dict = copy.deepcopy(self.test_tag_data)
        serializer_data["name"] = allowed_characters
        serializer: TagSerializer = TagSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], allowed_characters)

    def test_tag_serializer_name_regex_validator_fail(self):
        allowed_characters: str = "abcdefghijklmnopqrstuvwxyz "
        serializer_data: dict = copy.deepcopy(self.test_tag_data)
        serializer_data["name"] = allowed_characters + "#"
        serializer: TagSerializer = TagSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_tag_serializer_desc_max_length_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_tag_data)
        serializer_data["description"] = "e" * 201
        serializer: TagSerializer = TagSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"description"})

    def test_tag_serializer_desc_blank_pass(self):
        serializer_data: dict = copy.deepcopy(self.test_tag_data)
        serializer_data["description"] = ""
        serializer: TagSerializer = TagSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["description"], "")

    def test_tag_serializer_desc_regex_validator_pass_1(self):
        allowed_characters: str = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,# .!"
        )
        serializer_data: dict = copy.deepcopy(self.test_tag_data)
        serializer_data["description"] = allowed_characters
        serializer: TagSerializer = TagSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["description"], allowed_characters)

    def test_product_serializer_desc_regex_validator_fail(self):
        allowed_characters: str = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,# .!"
        )
        serializer_data: dict = copy.deepcopy(self.test_tag_data)
        serializer_data["description"] = allowed_characters + "*"
        serializer: TagSerializer = TagSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"description"})
