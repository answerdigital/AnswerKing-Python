from decimal import Decimal

from answerking_app.models.models import Category, Item, Order, Status
from answerking_app.utils.model_types import (
    CategoryType,
    DetailError,
    ItemType,
    OrderItemType,
    OrderType,
)


class TestBase:
    expected_serializer_error_400: DetailError = {
        "detail": "Validation Error",
        "errors": {},
        "status": 400,
        "title": "Invalid input.",
        "type": "http://testserver/problems/error/",
    }
    expected_base_json_parsing_error_400: DetailError = {
        "detail": "Parsing JSON Error",
        "errors": "JSON parse error - Expecting value: line 1 column 13 (char 12)",
        "status": 400,
        "title": "Invalid input json.",
        "type": "http://testserver/problems/error/",
    }
    expected_item_already_in_category: DetailError = {
        "detail": "Item is already in the category",
        "status": 400,
        "title": "A server error occurred.",
        "type": "http://testserver/problems/error/",
    }

    expected_base_404: DetailError = {
        "detail": "Not Found",
        "status": 404,
        "title": "Resource not found",
        "type": "http://testserver/problems/not_found/",
    }
    expected_duplicated_name_error: DetailError = {
        "detail": "This name already exists",
        "status": 400,
        "title": "A server error occurred.",
        "type": "http://testserver/problems/error/",
    }
    expected_invalid_status = {
        "detail": "Object was not Found",
        "errors": ["Status matching query does not exist."],
        "status": 404,
        "title": "Resource not found",
        "type": "http://testserver/problems/error/",
    }

    post_mock_item: ItemType = {
        "name": "Whopper",
        "price": "1.50",
        "description": "desc",
        "stock": 100,
        "calories": 100,
    }

    invalid_json_data: str = '{"invalid": }'

    def setUp(self):
        self.test_item_1: Item = Item.objects.create(
            name="Burger",
            price=1.20,
            description="desc",
            stock=100,
            calories=100,
        )
        self.test_item_2: Item = Item.objects.create(
            name="Coke",
            price=1.50,
            description="desc",
            stock=100,
            calories=100,
        )
        self.test_item_3: Item = Item.objects.create(
            name="Chips",
            price=1.50,
            description="desc",
            stock=100,
            calories=100,
        )

        self.test_cat_1: Category = Category.objects.create(name="Burgers")
        self.test_cat_2: Category = Category.objects.create(name="Sides")

        self.test_cat_1.items.add(self.test_item_1)
        self.test_cat_1.items.add(self.test_item_2)
        self.status_pending: Status = Status.objects.create(status="Pending")
        self.status_complete: Status = Status.objects.create(
            status="Completed"
        )

        self.test_order_empty: Order = Order.objects.create(
            address="123A3 Street, Leeds, LS17PP",
            status=self.status_pending,
        )

        self.test_order_1: Order = Order.objects.create(
            address="123 Street, Leeds, LS73PP",
            status=self.status_pending,
        )

        self.test_order_2: Order = Order.objects.create(
            address="456 Test Lane, Bradford, BD30PA",
            status=self.status_pending,
        )

        self.test_order_1.order_items.add(
            self.test_item_1,
            through_defaults={
                "quantity": 2,
                "sub_total": f"{self.test_item_1.price * 2:.2f}",
            },
        )

        self.test_order_1.order_items.add(
            self.test_item_2,
            through_defaults={
                "quantity": 1,
                "sub_total": f"{self.test_item_2.price:.2f}",
            },
        )
        self.test_order_1.calculate_total()

    def tearDown(self):
        Item.objects.all().delete()
        Category.objects.all().delete()
        Status.objects.all().delete()
        Order.objects.all().delete()

    def assertJSONResponse(self, expected, actual, response, status_code):
        self.assertEqual(expected, actual)  # type: ignore[reportGeneralTypeIssues]
        self.assertEqual(response.status_code, status_code)  # type: ignore[reportGeneralTypeIssues]

    def assertJSONErrorResponse(self, expected, actual, response, status_code):
        self.assertIsInstance(actual.pop("traceId"), str)  # type: ignore[reportGeneralTypeIssues]
        self.assertJSONResponse(expected, actual, response, status_code)

    def get_mock_item_api(self, item: Item) -> ItemType:
        return {
            "id": item.id,
            "name": item.name,
            "price": f"{item.price:.2f}",
            "description": item.description,
            "stock": item.stock,
            "calories": item.calories,
            "retired": False,
        }

    def get_mock_category_api(
        self, category: Category, items: list[ItemType] = []
    ) -> CategoryType:
        return {
            "id": category.id,
            "name": category.name,
            "items": items,
            "retired": False,
        }

    def get_mock_order_item_api(
        self, item: Item, quantity: int
    ) -> OrderItemType:
        return {
            "id": item.id,
            "name": item.name,
            "price": f"{item.price:.2f}",
            "quantity": quantity,
            "sub_total": f"{(item.price * quantity):.2f}",
        }

    def get_mock_order_api(
        self, order: Order, status: Status, items=[]
    ) -> OrderType:
        return {
            "id": order.id,
            "address": order.address,
            "status": status.status,
            "order_items": items,
            "total": f"{(sum(Decimal(item['sub_total']) for item in items)):.2f}",
        }
