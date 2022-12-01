import copy
from unittest import mock

from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Product, Category
from answerking_app.models.serializers import (
    CategoryDetailSerializer,
)
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails


class SerializerTests(UnitTestBase):
    UTB = UnitTestBase()

    serializer_path: str = 'answerking_app.models.serializers.'
    models_path: str = 'answerking_app.models.models.'
    test_cat_det_serializer_data: dict[str | None] = UTB.get_fixture(
        "categories",
        "cat_with_id_data.json"
    )
    test_cat_det_serializer: CategoryDetailSerializer = CategoryDetailSerializer(test_cat_det_serializer_data)

    # def setUp(self):
    #     Product.objects.create(**self.test_prod_1_data)
    #     Product.objects.create(**self.test_prod_2_data)
    #     Category.objects.create(**self.test_cat_1_data)
    #     retired_cat = Category.objects.create(**self.test_retired_cat_2_data)
    #     retired_cat.retired = True
    #     retired_cat.save()
    #
    # def tearDown(self):
    #     Product.objects.all().delete()
    #     Category.objects.all().delete()

    def test_cat_det_serializer_contains_correct_fields(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description'])

    def test_cat_det_serializer_id_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        expected: int = self.test_cat_det_serializer_data['id']
        actual: int = data['id']
        self.assertEqual(actual, expected)

    def test_cat_det_serializer_name_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        expected: str = self.test_cat_det_serializer_data['name']
        actual: str = data['name']
        self.assertEqual(actual, expected)

    def test_cat_det_serializer_name_max_length_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_cat_det_serializer_data)
        serializer_data['name']: str = 'e'*51
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'name'})

    def test_cat_det_serializer_name_blank_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_cat_det_serializer_data)
        serializer_data['name']: str = ''
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'name'})

    def test_cat_det_serializer_name_regex_validator_pass_1(self):
        allowed_characters: str = 'abcdefghijklm nopqrstuvwxyz'
        serializer_data: dict = copy.deepcopy(self.test_cat_det_serializer_data)
        serializer_data['name']: str = allowed_characters
        serializer = CategoryDetailSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['name'], allowed_characters)

    def test_cat_det_serializer_name_regex_validator_pass_2(self):
        allowed_characters: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!'
        serializer_data: dict = copy.deepcopy(self.test_cat_det_serializer_data)
        serializer_data['name']: str = allowed_characters
        serializer = CategoryDetailSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['name'], allowed_characters)

    def test_cat_det_serializer_name_regex_validator_fail(self):
        allowed_characters: str = 'abcdefghijklmnopqrstuvwxyz '
        serializer_data: dict = copy.deepcopy(self.test_cat_det_serializer_data)
        serializer_data['name']: str = allowed_characters + '#'
        serializer = CategoryDetailSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'name'})

    def test_cat_det_serializer_desc_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        actual: str = data['description']
        expected: str = self.test_cat_det_serializer_data['description']
        self.assertEqual(actual, expected)

    def test_cat_det_serializer_desc_max_length_fail(self):
        serializer_data: dict = copy.deepcopy(self.test_cat_det_serializer_data)
        serializer_data['description']: str = 'e'*201
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'description'})

    def test_cat_det_serializer_desc_None_pass(self):
        serializer_data: dict[str | None] = copy.deepcopy(self.test_cat_det_serializer_data)
        serializer_data['description']: None = None
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['description'], None)

    def test_cat_det_serializer_desc_blank_pass(self):
        serializer_data: dict = copy.deepcopy(self.test_cat_det_serializer_data)
        serializer_data['description']: str = ''
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['description'], '')

    def test_cat_det_serializer_desc_regex_validator_pass_1(self):
        allowed_characters: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,# .!'
        serializer_data: dict = copy.deepcopy(self.test_cat_det_serializer_data)
        serializer_data['description']: str = allowed_characters
        serializer = CategoryDetailSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['description'], allowed_characters)

    def test_cat_det_serializer_desc_regex_validator_fail(self):
        allowed_characters: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,# .!'
        serializer_data: dict = copy.deepcopy(self.test_cat_det_serializer_data)
        serializer_data['description']: str = allowed_characters+'*'
        serializer = CategoryDetailSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'description'})

    @mock.patch(
        serializer_path + 'CategoryDetailSerializer.products_check',
        return_value=[]
    )
    def test_cat_det_create_fn_no_prods_pass(
        self,
        products_check_mock,
    ):
        cds: CategoryDetailSerializer = CategoryDetailSerializer()
        new_cat: Category = cds.create(self.test_cat_det_serializer_data)
        cat_in_db: Category = Category.objects.get(pk=new_cat.id)

        products_check_mock.assert_called_once()
        self.assertEqual(cat_in_db.name, self.test_cat_det_serializer_data['name'])
        self.assertEqual(cat_in_db.description, self.test_cat_det_serializer_data['description'])
        self.assertEqual(list(cat_in_db.products.all()), [])

    @mock.patch(
        serializer_path + 'CategoryDetailSerializer.products_check',
    )
    def test_cat_det_create_fn_two_prods_pass(
        self,
        products_check_mock,
    ):
        to_seed = {"margarita_pizza_data.json": "products",
                   "pepperoni_pizza_data.json": "products"
                   }
        seeded_data = self.seed_data(to_seed)
        products_check_mock.return_value = [
            Product.objects.get(pk=1),
            Product.objects.get(pk=2)
        ]
        cds: CategoryDetailSerializer = CategoryDetailSerializer()
        new_cat: Category = cds.create(self.test_cat_det_serializer_data)
        cat_in_db: Category = Category.objects.get(pk=new_cat.id)
        expected_prod_names = [data['name'] for data in seeded_data]
        actual_prod_names = [val['name'] for val in cat_in_db.products.values("name")]

        products_check_mock.assert_called_once()
        self.assertEqual(cat_in_db.name, self.test_cat_det_serializer_data['name'])
        self.assertEqual(cat_in_db.description, self.test_cat_det_serializer_data['description'])
        self.assertEqual(actual_prod_names, expected_prod_names)

    @mock.patch(
        serializer_path + 'CategoryDetailSerializer.products_check',
    )
    @mock.patch(
        models_path + 'Category.objects'
    )
    def test_cat_det_update_fn_retired_category_fail(
        self,
        products_check_mock,
        category_objects_mock
    ):
        category_objects_mock.retired.return_value = True
        category_objects_mock.get.return_value = category_objects_mock
        with self.assertRaises(ProblemDetails) as context:
            retired_cat = Category.objects.get(pk=2)
            cds = CategoryDetailSerializer()
            cds.update(retired_cat, self.test_cat_det_serializer_data)

        products_check_mock.assert_not_called()
        self.assertEqual(category_objects_mock.call_count, 2)
        self.assertRaises(ProblemDetails)
        self.assertEqual(context.exception.detail, "This category has been retired")
        self.assertEqual(context.exception.status_code, status.HTTP_410_GONE)

    def test_product_check_only_needs_products_pass(self):
        prod_1 = Product.objects.get(pk=1).values()
        validated_data: dict = {'products': [
            self.get_mock_product_api(self.prod_1),
            self.get_mock_product_api(self.prod_1),
        ]}
        cds = CategoryDetailSerializer()
        expected: list[Product] = [
            self.test_product_1,
            self.test_product_2,
        ]
        actual: list[Product] = cds.products_check(validated_data)

        self.assertEqual(actual, expected)

    def test_product_check_retired_product_fail(self):
        with self.assertRaises(ProblemDetails) as context:
            validated_data: dict = self.test_cat_det_serializer_data
            validated_data['products'] = [self.get_mock_product_api(self.test_product_retired)]
            cds = CategoryDetailSerializer()
            cds.products_check(validated_data)

        self.assertRaises(ProblemDetails)
        self.assertEqual(context.exception.status_code, status.HTTP_410_GONE)
        self.assertEqual(context.exception.detail, "This product has been retired")

