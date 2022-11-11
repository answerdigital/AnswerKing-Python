from django.test import Client, TestCase

from answerking_app.models.models import Item, Order, Status
from answerking_app.utils.model_types import (
    DetailError,
    OrderItemType,
    OrderType,
)

client = Client()


class OrderLineTests(TestCase):
    maxDiff = None

    def setUp(self):
        self.status_pending: Status = Status.objects.create(status="Pending")

        self.test_item_1: Item = Item.objects.create(
            name="Burger",
            price=2.50,
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

        self.test_order_1.order_items.add(
            self.test_item_1,
            through_defaults={
                "quantity": 2,
                "sub_total": f"{self.test_item_1.price * 2:.2f}",
            },
        )

    def tearDown(self):
        Item.objects.all().delete()
        Order.objects.all().delete()
        Status.objects.all().delete()

    def test_add_new_orderline_valid_returns_ok(self):
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
                    "sub_total": f"{self.test_item_1.price * 2:.2f}",
                },
                {
                    "id": self.test_item_2.id,
                    "name": self.test_item_2.name,
                    "price": f"{self.test_item_2.price:.2f}",
                    "quantity": 1,
                    "sub_total": "1.50",
                },
            ],
            "total": "6.50",
        }
        post_data: OrderItemType = {"quantity": 1}

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_2.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_update_existing_orderline_valid_returns_ok(self):
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
                    "quantity": 1,
                    "sub_total": f"{self.test_item_1.price:.2f}",
                }
            ],
            "total": "2.50",
        }
        post_data: OrderItemType = {"quantity": 1}

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_update_existing_orderline_zero_quantity_returns_ok(self):
        # Arrange
        expected: OrderType = {
            "id": self.test_order_1.id,
            "address": self.test_order_1.address,
            "status": self.status_pending.status,
            "order_items": [],
            "total": "0.00",
        }
        post_data: OrderItemType = {"quantity": 0}

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_update_existing_orderline_invalid_returns_bad_request(self):
        # Arrange
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {"quantity": ["A valid integer is required."]},
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        post_data: OrderItemType = {"quantity": "f"}  # type: ignore[reportGeneralTypeIssues]

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_update_existing_orderline_negative_returns_bad_request(self):
        # Arrange
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {
                "quantity": [
                    "Ensure this value is greater than or equal to 0."
                ]
            },
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }
        post_data: OrderItemType = {"quantity": -1}

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_nonexistant_orderid_returns_not_found(self):
        # Arrange
        expected: DetailError = {
            "detail": "Not Found",
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.put(
            f"/api/orders/10000/orderline/{self.test_item_2.id}",
            {},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_itemid_returns_not_found(self):
        # Arrange
        expected: DetailError = {
            "detail": "Not Found",
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/100000",
            {},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_invalid_orderid_returns_not_found(self):
        # Arrange
        expected: DetailError = {
            "detail": "Not Found",
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/not_found/",
        }

        # Act
        response = client.put(
            f"/api/orders/f/orderline/{self.test_item_2.id}",
            {},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_invalid_itemid_returns_not_found(self):
        # Arrange
        expected: DetailError = {
            "detail": "Not Found",
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/not_found/",
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/f",
            {},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_delete_valid_returns_ok(self):
        # Arrange
        expected: OrderType = {
            "id": self.test_order_1.id,
            "address": self.test_order_1.address,
            "status": self.status_pending.status,
            "order_items": [],
            "total": "0.00",
        }

        # Act
        response = client.delete(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_1.id}"
        )
        actual = response.json()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, actual)

    def test_delete_nonexistant_id_returns_not_found(self):
        # Arrange
        expected: DetailError = {
            "detail": "A server error occurred.",
            "status": 404,
            "title": "A server error occurred.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.delete(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_3.id}"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)
