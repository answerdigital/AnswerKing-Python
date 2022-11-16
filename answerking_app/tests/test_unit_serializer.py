from django.test import TestCase

from answerking_app.models.models import Item, Category
from answerking_app.models.serializers import (
    compress_white_spaces,
    ItemSerializer,
    CategorySerializer,
)
from answerking_app.tests.BaseTestClass import TestBase
from answerking_app.utils.model_types import ItemType


class SerializerTests(TestBase, TestCase):

    def test_compress_white_spaces_fn(self):
        test_str: str = "  White   Spaces    "
        expected: str = "White Spaces"
        actual: str = compress_white_spaces(test_str)

        self.assertEqual(expected, actual)

    def test_regex_validator_raises_error(self):
        invalid_name_item: ItemType = self.post_mock_item
        invalid_name_item["name"] = "new_name"
        serialized_item: ItemSerializer = ItemSerializer(
            data=invalid_name_item
        )

        expected_error: str = "Enter a valid value."
        # needed to access .errors
        actual_error = 'name valid'
        if not serialized_item.is_valid():
            actual_error = serialized_item.errors["name"][0]

        self.assertEqual(expected_error, actual_error)

    def test_items_check_fn_only_depends_on_item_ids(self):
        rand_item_data: ItemType = self.post_mock_item
        rand_item_data["id"] = self.test_item_1.id
        mock_validated_data = {"items": [rand_item_data]}

        expected_items: list[Item] = [self.test_item_1]
        cs: CategorySerializer = CategorySerializer()
        actual_items: list[Item] = cs.items_check(validated_data=mock_validated_data)

        self.assertEqual(expected_items, actual_items)

    def test_cat_serializer_update_retired_field_supplied(self):
        mock_data: dict = {"retired": True}
        expected_retired_val: bool = True
        cs: CategorySerializer = CategorySerializer()

        cs.update(self.test_cat_1, mock_data)
        actual_retired_val: bool = self.test_cat_1.retired

        self.assertEqual(expected_retired_val, actual_retired_val)
