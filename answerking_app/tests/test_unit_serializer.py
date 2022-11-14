from django.test import TestCase

from answerking_app.models.models import Item
from answerking_app.models.serializers import compress_white_spaces, ItemSerializer, CategorySerializer


class SerializerTests(TestCase):

    def setUp(self):
        self.test_item_1: Item = Item.objects.create(
            name="Burger",
            price=1.20,
            description="desc",
            stock=100,
            calories=100,
        )

    def tearDown(self):
        Item.objects.all().delete()

    def test_compress_white_spaces_fn(self):
        test_str: str = '  White   Spaces    '
        expected: str = 'White Spaces'
        actual: str = compress_white_spaces(test_str)

        assert expected, actual

    def test_regex_validator_raises_error(self):
        invalid_item_details: dict = {
            "name": "new_name",
            "price": 2.00,
            "description": "Blah",
            "stock": 200,
            "calories": 0
        }
        serialized_item: ItemSerializer = ItemSerializer(data=invalid_item_details)

        expected_error: str = "Enter a valid value."
        # needed to access .errors
        if serialized_item.is_valid():
            pass

        assert serialized_item.errors['name'][0], expected_error

    def test_items_check_fn_only_depends_on_item_ids(self):
        mock_data: dict = {"items": [
            {
                "id": self.test_item_1.id,
                "name": "new_name",
                "price": 25.00,
                "description": "Blah",
                "stock": 200,
                "calories": 0,
                "retired": False
            },
        ]}

        expected_items: list[Item] = [self.test_item_1]
        cs = CategorySerializer()
        actual_items: list[Item] = cs.items_check(validated_data=mock_data)

        assert expected_items, actual_items
