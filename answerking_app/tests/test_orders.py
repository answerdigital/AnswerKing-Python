from django.db.models import QuerySet
from django.test import Client, TestCase
from rest_framework.exceptions import ParseError

from answerking_app.models.models import Item, Order, OrderLine, Status
from answerking_app.utils.ErrorType import ErrorMessage
from answerking_app.utils.model_types import (
    DetailError,
    OrderItemType,
    OrderType,
)

client = Client()


class OrderTests(TestCase):
    maxDiff = None

    def setUp(self):
        self.status_pending: Status = Status.objects.create(status="Pending")
        self.status_complete: Status = Status.objects.create(
            status="Completed"
        )

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

        self.test_order_1: Order = Order.objects.create(
            address="123 Street, Leeds, LS73PP",
            status=self.status_pending,
            total=7.50,
        )
        self.test_order_2: Order = Order.objects.create(
            address="456 Test Lane, Bradford, BD30PA",
            status=self.status_pending,
        )

        self.test_order_1.order_items.add(
            self.test_item_1, through_defaults={"quantity": 2, "sub_total": 5}
        )
        self.test_order_1.order_items.add(
            self.test_item_2,
            through_defaults={"quantity": 1, "sub_total": 2.5},
        )

    def tearDown(self):
        Item.objects.all().delete()
        Order.objects.all().delete()
        Status.objects.all().delete()

    def test_get_all_without_orders_returns_no_content(self):
        # Arrange
        Order.objects.all().delete()

        # Act
        response = client.get("/api/orders")

        # Assert
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 200)

    def test_get_all_with_orders_returns_ok(self):
        # Arrange
        expected: list[OrderType] = [
            {
                "id": self.test_order_1.id,
                "address": self.test_order_1.address,
                "status": self.status_pending.status,
                "order_items": [
                    {
                        "id": self.test_item_1.id,
                        "name": self.test_item_1.name,
                        "price": f"{self.test_item_1.price:.2f}",
                        "quantity": 2,
                        "sub_total": "5.00",
                    },
                    {
                        "id": self.test_item_2.id,
                        "name": self.test_item_2.name,
                        "price": f"{self.test_item_2.price:.2f}",
                        "quantity": 1,
                        "sub_total": "2.50",
                    },
                ],
                "total": "7.50",
            },
            {
                "id": self.test_order_2.id,
                "address": self.test_order_2.address,
                "status": "Pending",
                "order_items": [],
                "total": "0.00",
            },
        ]

        # Act
        response = client.get("/api/orders")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_get_id_valid_returns_ok(self):
        # Arrange
        expected: OrderType = {
            "id": self.test_order_1.id,
            "address": self.test_order_1.address,
            "status": self.status_pending.status,
            "order_items": [
                {
                    "id": self.test_item_1.id,
                    "name": self.test_item_1.name,
                    "price": f"{self.test_item_1.price:.2f}",
                    "quantity": 2,
                    "sub_total": "5.00",
                },
                {
                    "id": self.test_item_2.id,
                    "name": self.test_item_2.name,
                    "price": f"{self.test_item_2.price:.2f}",
                    "quantity": 1,
                    "sub_total": "2.50",
                },
            ],
            "total": "7.50",
        }

        # Act
        response = client.get(f"/api/orders/{self.test_order_1.id}")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_get_id_invalid_returns_not_found(self):
        # Arrange
        expected: DetailError = {
            "detail": "Not Found",
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/not_found/",
        }

        # Act
        response = client.get("/api/orders/f")
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_post_valid_without_items_returns_ok(self):
        # Arrange
        old_list = client.get("/api/orders").json()

        post_data: OrderType = {"address": "test street 123"}
        expected: OrderType = {
            "id": self.test_order_2.id + 1,
            "status": self.status_pending.status,
            "order_items": [],
            "total": "0.00",
            **post_data,
        }

        # Act
        response = client.post(
            "/api/orders", post_data, content_type="application/json"
        )
        actual = response.json()

        created_order: Order = Order.objects.get(pk=self.test_order_2.id + 1)
        created_order_items: list[OrderLine] = actual["order_items"]
        updated_list: QuerySet[Order] = Order.objects.all()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(created_order, updated_list)
        self.assertEqual(len(created_order_items), 0)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 201)

    def test_post_valid_with_empty_items_returns_ok(self):
        # Arrange
        old_list = client.get("/api/orders").json()

        post_data: OrderType = {
            "address": "test street 123",
            "order_items": [],
        }
        expected: OrderType = {
            "id": self.test_order_2.id + 1,
            "status": self.status_pending.status,
            "total": "0.00",
            **post_data,
        }

        # Act
        response = client.post(
            "/api/orders", post_data, content_type="application/json"
        )
        actual = response.json()

        created_order: Order = Order.objects.get(pk=self.test_order_2.id + 1)
        created_order_items: list[OrderLine] = actual["order_items"]
        updated_list: QuerySet[Order] = Order.objects.all()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(created_order, updated_list)
        self.assertEqual(len(created_order_items), 0)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 201)

    def test_post_valid_with_items_returns_ok(self):
        # Arrange
        old_list = client.get("/api/orders").json()

        order_item: OrderItemType = {
            "id": self.test_item_3.id,
            "name": self.test_item_3.name,
            "price": f"{self.test_item_3.price:.2f}",
            "quantity": 1,
            "sub_total": f"{self.test_item_3.price:.2f}",
        }
        post_data: OrderType = {
            "address": "test street 123",
            "order_items": [order_item],
        }

        expected: OrderType = {
            "id": self.test_order_2.id + 1,
            "status": self.status_pending.status,
            "total": f"{self.test_item_3.price:.2f}",
            **post_data,
        }

        # Act
        response = client.post(
            "/api/orders", post_data, content_type="application/json"
        )
        actual = response.json()

        created_order: Order = Order.objects.get(pk=self.test_order_2.id + 1)
        created_order_items: list[OrderLine] = actual["order_items"]
        updated_list: QuerySet[Order] = Order.objects.all()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(created_order, updated_list)
        self.assertIn(order_item, created_order_items)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 201)

    def test_post_invalid_json_returns_bad_request(self):
        # Arrange
        invalid_json_data: str = '{"invalid": }'
        expected: DetailError = {
            "detail": "Parsing JSON Error",
            "errors": "JSON parse error - Expecting value: line 1 column 13 (char 12)",
            "status": 400,
            "title": "Invalid input json.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/orders", invalid_json_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_details_returns_bad_request(self):
        # Arrange
        invalid_post_data: OrderType = {"address": "test%"}
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {"address": ["Enter a valid value."]},
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/orders", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_items_returns_bad_request(self):
        # Arrange
        invalid_post_data: OrderType = {
            "address": "test",
            "order_items": [{"values": "invalid"}],  # type: ignore
        }
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {
                "order_items": [{"quantity": ["This field is required."]}]
            },
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/orders", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_put_valid_address_and_status_returns_ok(self):
        # Arrange
        old_order = client.get(f"/api/orders/{self.test_order_1.id}").json()
        post_data: OrderType = {
            "address": "test",
            "status": self.status_complete.status,
        }
        expected: OrderType = {
            "id": self.test_order_1.id,
            **post_data,
            "order_items": [
                {
                    "id": self.test_item_1.id,
                    "name": self.test_item_1.name,
                    "price": f"{self.test_item_1.price:.2f}",
                    "quantity": 2,
                    "sub_total": "5.00",
                },
                {
                    "id": self.test_item_2.id,
                    "name": self.test_item_2.name,
                    "price": f"{self.test_item_2.price:.2f}",
                    "quantity": 1,
                    "sub_total": "2.50",
                },
            ],
            "total": "7.50",
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        updated_order: Order = Order.objects.get(pk=self.test_order_1.id)
        updated_list: QuerySet[Order] = Order.objects.all()

        # Assert
        self.assertNotEqual(old_order, actual)
        self.assertIn(updated_order, updated_list)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_put_valid_address_returns_ok(self):
        # Arrange
        old_order = client.get(f"/api/orders/{self.test_order_1.id}").json()
        post_data: OrderType = {"address": "test"}
        expected: OrderType = {
            "id": self.test_order_1.id,
            **post_data,
            "status": self.status_pending.status,
            "order_items": [
                {
                    "id": self.test_item_1.id,
                    "name": self.test_item_1.name,
                    "price": f"{self.test_item_1.price:.2f}",
                    "quantity": 2,
                    "sub_total": "5.00",
                },
                {
                    "id": self.test_item_2.id,
                    "name": self.test_item_2.name,
                    "price": f"{self.test_item_2.price:.2f}",
                    "quantity": 1,
                    "sub_total": "2.50",
                },
            ],
            "total": "7.50",
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        updated_order: Order = Order.objects.get(pk=self.test_order_1.id)
        updated_list: QuerySet[Order] = Order.objects.all()

        # Assert
        self.assertNotEqual(old_order, actual)
        self.assertIn(updated_order, updated_list)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_put_valid_status_returns_ok(self):
        # Arrange
        old_order = client.get(f"/api/orders/{self.test_order_1.id}").json()
        post_data: OrderType = {
            "status": self.status_complete.status,
        }
        expected: OrderType = {
            "id": self.test_order_1.id,
            "address": self.test_order_1.address,
            **post_data,
            "order_items": [
                {
                    "id": self.test_item_1.id,
                    "name": self.test_item_1.name,
                    "price": f"{self.test_item_1.price:.2f}",
                    "quantity": 2,
                    "sub_total": "5.00",
                },
                {
                    "id": self.test_item_2.id,
                    "name": self.test_item_2.name,
                    "price": f"{self.test_item_2.price:.2f}",
                    "quantity": 1,
                    "sub_total": "2.50",
                },
            ],
            "total": "7.50",
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        updated_order: Order = Order.objects.get(pk=self.test_order_1.id)
        updated_list: QuerySet[Order] = Order.objects.all()

        # Assert
        self.assertNotEqual(old_order, actual)
        self.assertIn(updated_order, updated_list)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_put_invalid_address_returns_bad_request(self):
        # Arrange
        invalid_post_data: OrderType = {"address": "test&"}
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {"address": ["Enter a valid value."]},
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_put_invalid_status_returns_not_found(self):
        # Arrange
        invalid_post_data: OrderType = {
            "address": "test",
            "status": "invalid",
        }
        expected: DetailError = {
            "detail": "Object was not Found",
            "errors": ["Status matching query does not exist."],
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_delete_valid_returns_ok(self):
        # Arrange
        order: Order = Order.objects.filter(pk=self.test_order_1.id)

        # Act
        response = client.delete(f"/api/orders/{self.test_order_1.id}")
        orders: QuerySet[Order] = Order.objects.all()

        # Assert
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(order, orders)

    def test_delete_invalid_id_returns_not_found(self):
        # Arrange
        expected: DetailError = {
            "detail": "Not Found",
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/not_found/",
        }

        # Act
        response = client.delete("/api/orders/f")
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)
