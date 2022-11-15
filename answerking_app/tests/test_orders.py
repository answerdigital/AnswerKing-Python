from django.db.models import QuerySet
from django.test import Client, TestCase

from answerking_app.models.models import Item, Order, OrderLine, Status
from answerking_app.tests.BaseTestClass import TestBase
from answerking_app.utils.model_types import (
    DetailError,
    OrderItemType,
    OrderType,
)

client = Client()


class OrderTests(TestBase, TestCase):
    maxDiff = None

    def test_get_all_without_orders_returns_no_content(self):
        # Arrange
        Order.objects.all().delete()

        # Act
        response = client.get("/api/orders")

        # Assert
        self.assertJSONResponse([], response.data, response, 200)

    def test_get_all_with_orders_returns_ok(self):
        # Arrange
        expected: list[OrderType] = [
            self.get_mock_order_api(
                self.test_order_empty, self.status_pending
            ),
            self.get_mock_order_api(
                self.test_order_1,
                self.status_pending,
                [
                    self.get_mock_order_item_api(self.test_item_1, 2),
                    self.get_mock_order_item_api(self.test_item_2, 1),
                ],
            ),
            self.get_mock_order_api(self.test_order_2, self.status_pending),
        ]

        # Act
        response = client.get("/api/orders")
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_get_id_valid_returns_ok(self):
        # Arrange
        expected: OrderType = self.get_mock_order_api(
            self.test_order_1,
            self.status_pending,
            [
                self.get_mock_order_item_api(self.test_item_1, 2),
                self.get_mock_order_item_api(self.test_item_2, 1),
            ],
        )

        # Act
        response = client.get(f"/api/orders/{self.test_order_1.id}")
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_get_id_invalid_returns_not_found(self):
        # Arrange
        response = client.get("/api/orders/f")
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )

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
        self.assertJSONResponse(expected, actual, response, 201)

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
        self.assertJSONResponse(expected, actual, response, 201)

    def test_post_valid_with_items_returns_ok(self):
        # Arrange
        old_list = client.get("/api/orders").json()

        order_item: OrderItemType = self.get_mock_order_item_api(
            self.test_item_3, 1
        )
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
        self.assertJSONResponse(expected, actual, response, 201)

    def test_post_invalid_json_returns_bad_request(self):
        # Act
        response = client.post(
            "/api/orders",
            self.invalid_json_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_json_parsing_error_400, actual, response, 400
        )

    def test_post_invalid_details_returns_bad_request(self):
        # Arrange
        invalid_post_data: OrderType = {"address": "test%"}
        expected: DetailError = {
            **self.expected_serializer_error_400,
            "errors": {"address": ["Enter a valid value."]},
        }

        # Act
        response = client.post(
            "/api/orders", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(expected, actual, response, 400)

    def test_post_invalid_items_returns_bad_request(self):
        # Arrange
        invalid_post_data: OrderType = {
            "address": "test",
            "order_items": [{"values": "invalid"}],  # type: ignore[reportGeneralTypeIssues]
        }
        expected: DetailError = {
            **self.expected_serializer_error_400,
            "errors": {
                "order_items": [{"quantity": ["This field is required."]}]
            },
        }

        # Act
        response = client.post(
            "/api/orders", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(expected, actual, response, 400)

    def test_put_valid_address_and_status_returns_ok(self):
        # Arrange
        old_order = client.get(f"/api/orders/{self.test_order_1.id}").json()
        post_data: OrderType = {
            "address": "test",
            "status": self.status_complete.status,
        }
        expected: OrderType = (
            self.get_mock_order_api(
                self.test_order_1,
                self.status_pending,
                [
                    self.get_mock_order_item_api(self.test_item_1, 2),
                    self.get_mock_order_item_api(self.test_item_2, 1),
                ],
            )
            | post_data
        )

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
        self.assertJSONResponse(expected, actual, response, 200)

    def test_put_valid_address_returns_ok(self):
        # Arrange
        old_order = client.get(f"/api/orders/{self.test_order_1.id}").json()
        post_data: OrderType = {"address": "test"}
        expected: OrderType = (
            self.get_mock_order_api(
                self.test_order_1,
                self.status_pending,
                [
                    self.get_mock_order_item_api(self.test_item_1, 2),
                    self.get_mock_order_item_api(self.test_item_2, 1),
                ],
            )
            | post_data
        )

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
        self.assertJSONResponse(expected, actual, response, 200)

    def test_put_valid_status_returns_ok(self):
        # Arrange
        old_order = client.get(f"/api/orders/{self.test_order_1.id}").json()
        post_data: OrderType = {
            "status": self.status_complete.status,
        }
        expected: OrderType = (
            self.get_mock_order_api(
                self.test_order_1,
                self.status_pending,
                [
                    self.get_mock_order_item_api(self.test_item_1, 2),
                    self.get_mock_order_item_api(self.test_item_2, 1),
                ],
            )
            | post_data
        )
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
        self.assertJSONResponse(expected, actual, response, 200)

    def test_put_invalid_address_returns_bad_request(self):
        # Arrange
        invalid_post_data: OrderType = {"address": "test&"}
        expected: DetailError = {
            **self.expected_serializer_error_400,
            "errors": {"address": ["Enter a valid value."]},
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(expected, actual, response, 400)

    def test_put_invalid_status_returns_not_found(self):
        # Arrange
        invalid_post_data: OrderType = {
            "address": "test",
            "status": "invalid",
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_invalid_status, actual, response, 404
        )

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
        # Act
        response = client.delete("/api/orders/f")
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )
