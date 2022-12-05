from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Category, Product
from answerking_app.models.serializers import CategorySerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class CategorySerializerUnitTests(UnitTestBase):
    UBT = UnitTestBase()
    test_cat_data: dict = UBT.get_fixture(
        "categories",
        "burgers_cat_data.json"
    )
    test_prod_data: dict = UBT.get_fixture(
        "products",
        "plain_burger_data.json"
    )

    def setUp(self):
        cat = Category.objects.create(**self.test_cat_data)
        prod = Product.objects.create(**self.test_prod_data)
        cat.products.add(prod)

    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()

    def test_cat_serializer_contains_correct_fields(self):
        test_cat = Category.objects.get(name=self.test_cat_data['name'])
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
        self.assertCountEqual(actual, expected)

    def test_cat_serializer_id_field_content(self):
        test_cat = Category.objects.get(name=self.test_cat_data['name'])
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: int = test_cat.id
        actual: int = test_serializer_data['id']
        self.assertEqual(actual, expected)

    def test_cat_serializer_name_field_content(self):
        test_cat = Category.objects.get(name=self.test_cat_data['name'])
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: int = test_cat.name
        actual: int = test_serializer_data['name']
        self.assertEqual(actual, expected)

    def test_cat_serializer_desc_field_content(self):
        test_cat = Category.objects.get(name=self.test_cat_data['name'])
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: int = test_cat.description
        actual: int = test_serializer_data['description']
        self.assertEqual(actual, expected)

    def test_cat_serializer_products_field_content(self):
        test_cat = Category.objects.get(name=self.test_cat_data['name'])
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: dict = dict(*test_cat.products.values('id'))
        actual: dict = dict(*test_serializer_data['products'])
        self.assertEqual(actual, expected)

    def test_cat_serializer_retired_field_content(self):
        test_cat = Category.objects.get(name=self.test_cat_data['name'])
        test_serializer_data: ReturnDict = CategorySerializer(test_cat).data
        expected: int = test_cat.retired
        actual: int = test_serializer_data['retired']
        self.assertEqual(actual, expected)
