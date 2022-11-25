from unittest import mock

from django.test import TestCase
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.models import Product, Category
from answerking_app.models.serializers import (
    compress_white_spaces,
    ProductSerializer,
    CategorySerializer,
    CategoryDetailSerializer,
)
from answerking_app.tests.BaseTestClass import TestBase
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails
from answerking_app.utils.model_types import ProductType


class SerializerTests(TestBase):

    serializer_path = 'answerking_app.models.serializers.'

    def test_compress_white_spaces_fn(self):
        test_str: str = "  White   Spaces    "
        expected: str = "White Spaces"
        actual: str = compress_white_spaces(test_str)

        self.assertEqual(expected, actual)

    def test_cat_det_serializer_contains_correct_fields(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description'])

    def test_cat_det_serializer_id_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        self.assertEqual(data['id'], self.test_cat_1.id)

    def test_cat_det_serializer_name_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        self.assertEqual(data['name'], self.test_cat_1.name)

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
        self.assertEqual(data['description'], self.test_cat_1.description)

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
        allowed_characters: str = 'abcdefghijklmnopqrstuvwxyz .!'
        serializer_data = self.cat_det_serializer_data
        serializer_data['description'] = allowed_characters
        serializer = CategoryDetailSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['description'], allowed_characters)

    def test_cat_det_serializer_desc_regex_validator_pass_2(self):
        allowed_characters: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ,#'
        serializer_data = self.cat_det_serializer_data
        serializer_data['description'] = allowed_characters
        serializer = CategoryDetailSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['description'], allowed_characters)

    def test_cat_det_serializer_desc_regex_validator_fail(self):
        allowed_characters: str = 'abcdefghijklmnopqrstuvwxyz '
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
        products_check_mock.return_value = [self.TB.test_product_1, self.TB.test_product_2]
        cds = CategoryDetailSerializer()
        new_cat = cds.create(self.cat_det_serializer_data)
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
        with self.assertRaises(ProblemDetails) as cm:
            retired_cat = self.test_cat_retired
            cds = CategoryDetailSerializer()
            cds.update(retired_cat, self.cat_det_serializer_data)

        products_check_mock.assert_not_called()
        self.assertRaises(ProblemDetails)
        self.assertEqual(cm.exception.detail, "This category has been retired")
        self.assertEqual(cm.exception.status_code, status.HTTP_410_GONE)
