from datetime import datetime

from django.db.models import QuerySet
from django.test import Client

from answerking_app.models.models import Order, LineItem
from answerking_app.tests.BaseTestClass import TestBase
from answerking_app.utils.model_types import (
    DetailError,
    OrderType,
)

client = Client()


class OrderTests(TestBase):
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
            self.get_mock_order_api(self.test_order_empty),
            self.get_mock_order_api(
                self.test_order_1,
            ),
            self.get_mock_order_api(self.test_order_2),
        ]

        # Act
        response = client.get("/api/orders")
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_get_id_valid_returns_ok(self):
        # Arrange
        expected: OrderType = self.get_mock_order_api(self.test_order_1)

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

    def test_post_valid_without_products_returns_ok(self):
        # Arrange
        old_list = client.get("/api/orders").json()

        post_data: dict = {}
        expected: OrderType = {
            "id": self.test_order_2.id + 1,
            "createdOn": datetime.now(),
            "lastUpdated": datetime.now(),
            "orderStatus": "Created",
            "orderTotal": 0.00,
            "lineItems": [],
        }

        # Act
        response = client.post(
            "/api/orders", post_data, content_type="application/json"
        )
        actual = response.json()

        created_order: Order = Order.objects.get(pk=self.test_order_2.id + 1)
        created_order_products: list[LineItem] = actual["lineItems"]
        updated_list: QuerySet[Order] = Order.objects.all()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(created_order, updated_list)
        self.assertEqual(len(created_order_products), 0)
        self.assertCreateUpdateTime(expected, actual, response, 201)

    def test_post_valid_with_empty_products_returns_ok(self):
        # Arrange
        old_list = client.get("/api/orders").json()

        post_data: dict = {
            "lineItems": [],
        }
        expected: dict = {
            "id": self.test_order_2.id + 1,
            "createdOn": datetime.now(),
            "lastUpdated": datetime.now(),
            "orderStatus": "Created",
            "orderTotal": 0.00,
            **post_data,
        }

        # Act
        response = client.post(
            "/api/orders", post_data, content_type="application/json"
        )
        actual = response.json()

        created_order_products: list[LineItem] = actual["lineItems"]
        updated_list = client.get("/api/orders").json()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(actual, updated_list)
        self.assertEqual(len(created_order_products), 0)
        self.assertCreateUpdateTime(expected, actual, response, 201)

    def test_post_valid_with_products_returns_ok(self):
        # Arrange
        old_orders_list_json = client.get("/api/orders").json()
        post_data = {
            "lineItems": [
                {"product": {"id": self.test_product_1.id}, "quantity": 1}
            ]
        }
        expected: OrderType = {
            "id": self.test_order_2.id + 1,
            "createdOn": datetime.now(),
            "lastUpdated": datetime.now(),
            "orderStatus": "Created",
            "orderTotal": self.test_product_1.price,
            "lineItems": [
                {
                    "product": self.get_category_and_product_for_order(
                        self.test_product_1
                    ),
                    "quantity": 1,
                    "subTotal": self.test_product_1.price,
                }
            ],
        }
        # Act
        response = client.post(
            "/api/orders", post_data, content_type="application/json"
        )
        actual = response.json()

        updated_orders_list_json = client.get("/api/orders").json()
        updated_orders_objects: list[Order] = Order.objects.all()

        created_order: Order = Order.objects.get(pk=actual["id"])

        # Assert
        self.assertIn(created_order, updated_orders_objects)
        self.assertNotIn(actual, old_orders_list_json)
        self.assertIn(actual, updated_orders_list_json)
        self.assertCreateUpdateTime(
            expected, actual, response, status_code=201
        )

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
        invalid_post_data = {"lineItems": [{"id": "df"}]}
        expected: DetailError = {
            **self.expected_serializer_error_400,
            "errors": {
                "lineItems": [
                    {
                        "product": ["This field is required."],
                        "quantity": ["This field is required."],
                    }
                ]
            },
        }

        # Act
        response = client.post(
            "/api/orders", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(expected, actual, response, 400)

    def test_put_add_valid_products_to_order_return_ok(self):
        # Arrange
        old_orders_list_json = client.get("/api/orders").json()
        post_data = {
            "lineItems": [
                {"product": {"id": self.test_product_1.id}, "quantity": 1}
            ]
        }
        expected = self.expected_order_after_put_request(
            self.test_order_1, post_data["lineItems"]
        )

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        updated_orders_list_json = client.get("/api/orders").json()
        updated_orders_objects: list[Order] = Order.objects.all()

        created_order: Order = Order.objects.get(pk=actual["id"])

        # Assert
        self.assertIn(created_order, updated_orders_objects)
        self.assertNotIn(actual, old_orders_list_json)
        self.assertIn(actual, updated_orders_list_json)
        self.assertUpdateTime(expected, actual, response, status_code=200)

    def test_put_update_quantity_to_zero_return_empty_line_items(self):
        # Arrange
        old_orders_list_json = client.get("/api/orders").json()
        post_data = {
            "lineItems": [
                {"product": {"id": self.test_product_1.id}, "quantity": 0}
            ]
        }
        expected = {
            **self.expected_order_after_put_request(
                self.test_order_1, post_data["lineItems"]
            ),
        }
        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        updated_orders_list_json = client.get("/api/orders").json()
        updated_orders_objects: list[Order] = Order.objects.all()

        created_order: Order = Order.objects.get(pk=actual["id"])

        # Assert
        self.assertIn(created_order, updated_orders_objects)
        self.assertNotIn(actual, old_orders_list_json)
        self.assertIn(actual, updated_orders_list_json)
        self.assertUpdateTime(expected, actual, response, status_code=200)
        self.assertEqual(actual["lineItems"], [])

    def test_put_invalid_order_id_return_not_found(self):
        # Arrange
        post_data = {
            "lineItems": [
                {"product": {"id": self.test_product_1.id}, "quantity": 1}
            ]
        }
        # Act
        response = client.put(
            f"/api/orders/-1",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )

    def test_put_invalid_products_return_empty_order(self):
        # Arrange
        post_data = {"lineItems": [{"product": {"id": -1}, "quantity": 1}]}
        # Act
        response = client.put(
            f"/api/orders/{self.test_order_2.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_nonexistent_product_error, actual, response, 400
        )

    def test_delete_order_valid_returns_ok(self):
        # Arrange
        old_order_status: str = self.test_order_1.order_status
        expected_order_status: str = "Cancelled"
        # Act
        response = client.delete(f"/api/orders/{self.test_order_1.id}")
        updated_order_status = response.json()["orderStatus"]

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(old_order_status, updated_order_status)
        self.assertEqual(expected_order_status, updated_order_status)

    def test_delete_invalid_id_returns_not_found(self):
        # Arrange
        # Act
        response = client.delete("/api/orders/f")
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )
