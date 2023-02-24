from freezegun import freeze_time
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Product
from answerking_app.models.serializers import CategorySerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class CategorySerializerUnitTests(UnitTestBase):
    UTB = UnitTestBase()
    test_cat_data: dict = UTB.get_fixture(
        "categories", "burgers_cat_data.json"
    )
    test_prod_data: dict = UTB.get_fixture(
        "products", "plain_burger_data.json"
    )
    frozen_time: str = "2022-01-01T01:02:03.000000Z"

    @freeze_time(frozen_time)
    def setUp(self):
        cat: Category = Category.objects.create(**self.test_cat_data)
        prod: Product = Product.objects.create(**self.test_prod_data)
        cat.product_set.add(prod)

    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()

    def test_cat_serializer_contains_correct_fields(self):
        test_cat: Category = Category.objects.get(
            name=self.test_cat_data["name"]
        )
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: list[str] = [
            "id",
            "name",
            "description",
            "createdOn",
            "lastUpdated",
            "products",
            "retired",
        ]
        actual: list[str] = list(test_serializer_data.keys())
        self.assertEqual(actual, expected)

    def test_cat_serializer_id_field_content(self):
        test_cat: Category = Category.objects.get(
            name=self.test_cat_data["name"]
        )
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: int = test_cat.id
        actual: int = test_serializer_data["id"]
        self.assertEqual(actual, expected)

    def test_cat_serializer_name_field_content(self):
        test_cat: Category = Category.objects.get(
            name=self.test_cat_data["name"]
        )
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: str = test_cat.name
        actual: str = test_serializer_data["name"]
        self.assertEqual(actual, expected)

    def test_cat_serializer_desc_field_content(self):
        test_cat: Category = Category.objects.get(
            name=self.test_cat_data["name"]
        )
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: str = test_cat.description
        actual: str = test_serializer_data["description"]
        self.assertEqual(actual, expected)

    def test_cat_serializer_products_field_content(self):
        test_cat: Category = Category.objects.get(
            name=self.test_cat_data["name"]
        )
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: int = dict(*test_cat.product_set.values("id"))["id"]
        actual: int = test_serializer_data["products"][0]
        self.assertEqual(actual, expected)

    def test_cat_serializer_retired_field_content(self):
        test_cat: Category = Category.objects.get(
            name=self.test_cat_data["name"]
        )
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: bool = test_cat.retired
        actual: bool = test_serializer_data["retired"]
        self.assertEqual(actual, expected)

    @freeze_time(frozen_time)
    def test_cat_serializer_created_on_field_content(self):
        test_cat: Category = Category.objects.get(
            name=self.test_cat_data["name"]
        )
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: str = self.frozen_time
        actual: str = test_serializer_data["createdOn"]
        self.assertEqual(actual, expected)

    def test_cat_serializer_last_updated_field_content(self):
        test_cat: Category = Category.objects.get(
            name=self.test_cat_data["name"]
        )
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: str = self.frozen_time
        actual: str = test_serializer_data["lastUpdated"]
        self.assertEqual(actual, expected)
