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


class CategoryDetailSerializerUnitTests(UnitTestBase):
    UTB = UnitTestBase()
    serializer_path: str = "answerking_app.models.serializers."
    models_path: str = "answerking_app.models.models."
    test_cat_det_serializer_data: dict = UTB.get_fixture(
        "categories", "cat_with_id_data.json"
    )
    test_cat_det_serializer: CategoryDetailSerializer = (
        CategoryDetailSerializer(test_cat_det_serializer_data)
    )

    def test_cat_det_serializer_contains_correct_fields(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        expected: list[str] = ["id", "name", "description"]
        actual: list[str] = list(data.keys())
        self.assertEqual(actual, expected)

    def test_cat_det_serializer_id_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        expected: int = self.test_cat_det_serializer_data["id"]
        actual: int = data["id"]
        self.assertEqual(actual, expected)

    def test_cat_det_serializer_name_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        expected: str = self.test_cat_det_serializer_data["name"]
        actual: str = data["name"]
        self.assertEqual(actual, expected)

    def test_cat_det_serializer_name_max_length_fail(self):
        serializer_data: dict = copy.deepcopy(
            self.test_cat_det_serializer_data
        )
        serializer_data["name"] = "e" * 51
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(
            data=serializer_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_cat_det_serializer_name_blank_fail(self):
        serializer_data: dict = copy.deepcopy(
            self.test_cat_det_serializer_data
        )
        serializer_data["name"] = ""
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(
            data=serializer_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_cat_det_serializer_name_regex_validator_pass_1(self):
        allowed_characters: str = "abcdefghijklm nopqrstuvwxyz0123456789"
        serializer_data: dict = copy.deepcopy(
            self.test_cat_det_serializer_data
        )
        serializer_data["name"] = allowed_characters
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(
            data=serializer_data
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], allowed_characters)

    def test_cat_det_serializer_name_regex_validator_pass_2(self):
        allowed_characters: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!0123456789"
        serializer_data: dict = copy.deepcopy(
            self.test_cat_det_serializer_data
        )
        serializer_data["name"] = allowed_characters
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(
            data=serializer_data
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], allowed_characters)

    def test_cat_det_serializer_name_regex_validator_fail(self):
        allowed_characters: str = "abcdefghijklmnopqrstuvwxyz "
        serializer_data: dict = copy.deepcopy(
            self.test_cat_det_serializer_data
        )
        serializer_data["name"] = allowed_characters + "#"
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(
            data=serializer_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name"})

    def test_cat_det_serializer_desc_field_content(self):
        data: ReturnDict = self.test_cat_det_serializer.data
        actual: str = data["description"]
        expected: str = self.test_cat_det_serializer_data["description"]
        self.assertEqual(actual, expected)

    def test_cat_det_serializer_desc_max_length_fail(self):
        serializer_data: dict = copy.deepcopy(
            self.test_cat_det_serializer_data
        )
        serializer_data["description"] = "e" * 201
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(
            data=serializer_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"description"})

    def test_cat_det_serializer_desc_None_pass(self):
        serializer_data: dict = copy.deepcopy(
            self.test_cat_det_serializer_data
        )
        serializer_data["description"] = None
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(
            data=serializer_data
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["description"], None)

    def test_cat_det_serializer_desc_blank_pass(self):
        serializer_data: dict = copy.deepcopy(
            self.test_cat_det_serializer_data
        )
        serializer_data["description"] = ""
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(
            data=serializer_data
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["description"], "")

    def test_cat_det_serializer_desc_regex_validator_pass_1(self):
        allowed_characters: str = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ",# .0123456789!"
        )
        serializer_data: dict = copy.deepcopy(
            self.test_cat_det_serializer_data
        )
        serializer_data["description"] = allowed_characters
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(
            data=serializer_data
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["description"], allowed_characters)

    def test_cat_det_serializer_desc_regex_validator_fail(self):
        allowed_characters: str = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ",# .0123456789!"
        )
        serializer_data: dict = copy.deepcopy(
            self.test_cat_det_serializer_data
        )
        serializer_data["description"] = allowed_characters + "*"
        serializer: CategoryDetailSerializer = CategoryDetailSerializer(
            data=serializer_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"description"})

    @mock.patch(
        serializer_path + "products_check",
        return_value=[],
    )
    def test_cat_det_create_fn_no_prods_pass(
        self,
        products_check_mock,
    ):
        cds: CategoryDetailSerializer = CategoryDetailSerializer()
        new_cat: Category = cds.create(self.test_cat_det_serializer_data)
        cat_in_db: Category = Category.objects.get(pk=new_cat.id)

        products_check_mock.assert_called_once()
        self.assertEqual(
            cat_in_db.name, self.test_cat_det_serializer_data["name"]
        )
        self.assertEqual(
            cat_in_db.description,
            self.test_cat_det_serializer_data["description"],
        )
        self.assertEqual(list(cat_in_db.product_set.all()), [])

    @mock.patch(
        serializer_path + "products_check",
    )
    def test_cat_det_create_fn_two_prods_pass(
        self,
        products_check_mock,
    ):
        to_seed: dict = {
            "margarita_pizza_data.json": "products",
            "pepperoni_pizza_data.json": "products",
        }
        seeded_data: list[dict] = self.seed_data(to_seed)
        products_check_mock.return_value = [
            Product.objects.get(name="Margarita pizza"),
            Product.objects.get(name="Pepperoni pizza"),
        ]
        cds: CategoryDetailSerializer = CategoryDetailSerializer()
        new_cat: Category = cds.create(self.test_cat_det_serializer_data)
        cat_in_db: Category = Category.objects.get(pk=new_cat.id)
        expected_prod_names: list[str] = [data["name"] for data in seeded_data]
        actual_prod_names: list[str] = [
            val["name"] for val in cat_in_db.product_set.values("name")
        ]

        products_check_mock.assert_called_once()
        self.assertEqual(
            cat_in_db.name, self.test_cat_det_serializer_data["name"]
        )
        self.assertEqual(
            cat_in_db.description,
            self.test_cat_det_serializer_data["description"],
        )
        self.assertEqual(actual_prod_names, expected_prod_names)

    @mock.patch(
        serializer_path + "products_check",
    )
    def test_cat_det_update_fn_retired_category_fail(
        self,
        products_check_mock,
    ):
        to_seed: dict = {"retired_cat_data.json": "categories"}
        self.seed_data(to_seed)
        with self.assertRaises(ProblemDetails) as context:
            retired_cat: Category = Category.objects.get(name="Old Burgers")
            cds: CategoryDetailSerializer = CategoryDetailSerializer()
            cds.update(retired_cat, self.test_cat_det_serializer_data)

        products_check_mock.assert_not_called()
        self.assertRaises(ProblemDetails)
        self.assertEqual(
            context.exception.detail, "This category has been retired"
        )
        self.assertEqual(context.exception.status_code, status.HTTP_410_GONE)

    @mock.patch(
        serializer_path + "products_check",
    )
    def test_cat_det_update_fn_pass(
        self,
        products_check_mock,
    ):
        to_seed: dict = {
            "margarita_pizza_data.json": "products",
            "pepperoni_pizza_data.json": "products",
            "pizzas_cat_data.json": "categories",
        }
        seeded_data: list[dict] = self.seed_data(to_seed)
        serialized_data: CategoryDetailSerializer = CategoryDetailSerializer(
            seeded_data[2]
        )
        products_check_mock.return_value = [
            Product.objects.get(name="Margarita pizza"),
            Product.objects.get(name="Pepperoni pizza"),
        ]
        cat: Category = Category.objects.get(name="Pizza")
        cds: CategoryDetailSerializer = CategoryDetailSerializer()
        updated_cat: Category = cds.update(cat, seeded_data[2])

        products_check_mock.assert_called_once()
        self.assertEqual(updated_cat.name, serialized_data.data["name"])
        self.assertEqual(
            updated_cat.description, serialized_data.data["description"]
        )
        self.assertEqual(
            list(updated_cat.product_set.all()),
            products_check_mock.return_value,
        )
