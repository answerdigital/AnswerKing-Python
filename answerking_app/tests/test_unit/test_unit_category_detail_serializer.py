from unittest import mock

from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Product, Category
from answerking_app.models.serializers import (
    CategoryDetailSerializer,
)
from answerking_app.tests.BaseTestClass import TestBase
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails


class SerializerTests(TestBase):

    serializer_path = 'answerking_app.models.serializers.'

    def test_cat_det_serializer_contains_correct_fields(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description'])

    def test_cat_det_serializer_id_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        self.assertEqual(data['id'], self.test_cat.id)

    def test_cat_det_serializer_name_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        self.assertEqual(data['name'], self.test_cat.name)

    def test_cat_det_serializer_name_max_length_fail(self):
        serializer_data = self.cat_det_serializer_data
        serializer_data['name'] = 'e'*51
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'name'})

    def test_cat_det_serializer_name_blank_fail(self):
        serializer_data = self.cat_det_serializer_data
        serializer_data['name'] = ''
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'name'})

    def test_cat_det_serializer_name_regex_validator_pass_1(self):
        allowed_characters: str = 'abcdefghijklm nopqrstuvwxyz'
        serializer_data = self.cat_det_serializer_data
        serializer_data['name'] = allowed_characters
        serializer = CategoryDetailSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['name'], allowed_characters)

    def test_cat_det_serializer_name_regex_validator_pass_2(self):
        allowed_characters: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!'
        serializer_data = self.cat_det_serializer_data
        serializer_data['name'] = allowed_characters
        serializer = CategoryDetailSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['name'], allowed_characters)

    def test_cat_det_serializer_name_regex_validator_fail(self):
        allowed_characters: str = 'abcdefghijklmnopqrstuvwxyz '
        serializer_data = self.cat_det_serializer_data
        serializer_data['name'] = allowed_characters + '#'
        serializer = CategoryDetailSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'name'})

    def test_cat_det_serializer_desc_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        self.assertEqual(data['description'], self.test_cat.description)

    def test_cat_det_serializer_desc_max_length_fail(self):
        serializer_data = self.cat_det_serializer_data
        serializer_data['description'] = 'e'*201
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'description'})

    def test_cat_det_serializer_desc_None_pass(self):
        serializer_data = self.cat_det_serializer_data
        serializer_data['description'] = None
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['description'], None)

    def test_cat_det_serializer_desc_blank_pass(self):
        serializer_data = self.cat_det_serializer_data
        serializer_data['description'] = ''
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['description'], '')

    def test_cat_det_serializer_desc_regex_validator_pass_1(self):
        allowed_characters: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,# .!'
        serializer_data = self.cat_det_serializer_data
        serializer_data['description'] = allowed_characters
        serializer = CategoryDetailSerializer(data=serializer_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['description'], allowed_characters)

    def test_cat_det_serializer_desc_regex_validator_fail(self):
        allowed_characters: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,# .!'
        serializer_data = self.cat_det_serializer_data
        serializer_data['description'] = allowed_characters+'*'
        serializer = CategoryDetailSerializer(data=serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'description'})

    @mock.patch(
        serializer_path + 'CategoryDetailSerializer.products_check',
    )
    def test_cat_det_create_fn_no_products_pass(self, products_check_mock):
        products_check_mock.return_value = []
        cds = CategoryDetailSerializer()
        new_cat = cds.create(self.cat_det_serializer_data)
        created_cat = Category.objects.get(pk=new_cat.id)
        products_check_mock.assert_called_once()

        self.assertEqual(created_cat.name, self.cat_det_serializer_data['name'])
        self.assertEqual(created_cat.description, self.cat_det_serializer_data['description'])
        self.assertEqual(list(created_cat.products.values()), [])

    @mock.patch(
        serializer_path + 'CategoryDetailSerializer.products_check',
    )
    def test_cat_det_create_fn_w_products_pass(self, products_check_mock):
        products_check_mock.return_value = [self.test_product_1, self.test_product_2]
        serializer_data = self.cat_det_serializer_data
        serializer_data['products'] = [
            self.get_mock_product_api(self.test_product_1),
            self.get_mock_product_api(self.test_product_2)
        ]
        cds = CategoryDetailSerializer()
        new_cat = cds.create(serializer_data)
        created_cat = Category.objects.get(pk=new_cat.id)
        expected_prod_ids = [self.test_product_1,
                             self.test_product_2
                             ]
        actual_prod_ids = list(created_cat.products.all())

        products_check_mock.assert_called_once()
        self.assertEqual(created_cat.name, self.cat_det_serializer_data['name'])
        self.assertEqual(created_cat.description, self.cat_det_serializer_data['description'])
        self.assertEqual(actual_prod_ids, expected_prod_ids)

    @mock.patch(
        serializer_path + 'CategoryDetailSerializer.products_check',
    )
    def test_cat_det_update_fn_retired_category_fail(self, products_check_mock):
        with self.assertRaises(ProblemDetails) as context:
            retired_cat = self.test_cat_retired
            cds = CategoryDetailSerializer()
            cds.update(retired_cat, self.cat_det_serializer_data)

        products_check_mock.assert_not_called()
        self.assertRaises(ProblemDetails)
        self.assertEqual(context.exception.detail, "This category has been retired")
        self.assertEqual(context.exception.status_code, status.HTTP_410_GONE)

    def test_product_check_only_needs_products_pass(self):
        validated_data: dict = {'products': [
            self.get_mock_product_api(self.test_product_1),
            self.get_mock_product_api(self.test_product_2),
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
            validated_data: dict = self.cat_det_serializer_data
            validated_data['products'] = [self.get_mock_product_api(self.test_product_retired)]
            cds = CategoryDetailSerializer()
            cds.products_check(validated_data)

        self.assertRaises(ProblemDetails)
        self.assertEqual(context.exception.status_code, status.HTTP_410_GONE)
        self.assertEqual(context.exception.detail, "This product has been retired")

