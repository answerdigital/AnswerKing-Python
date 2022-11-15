from django.test import Client, TestCase

from answerking_app.tests.BaseTestClass import TestBase
from answerking_app.utils.model_types import (
    DetailError,
    OrderItemType,
    OrderType,
)

client = Client()


class OrderLineTests(TestBase, TestCase):
    maxDiff: int | None = None

    def test_add_new_orderline_valid_returns_ok(self):
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
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_2.id}",
            {"quantity": 1},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_update_existing_orderline_valid_returns_ok(self):
        # Arrange
        expected: OrderType = self.get_mock_order_api(
            self.test_order_empty,
            self.status_pending,
            [self.get_mock_order_item_api(self.test_item_1, 1)],
        )

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_empty.id}/orderline/{self.test_item_1.id}",
            {"quantity": 1},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_update_existing_orderline_zero_quantity_returns_ok(self):
        # Arrange
        expected: OrderType = self.get_mock_order_api(
            self.test_order_empty, self.status_pending
        )

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_empty.id}/orderline/{self.test_item_1.id}",
            {"quantity": 0},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_update_existing_orderline_invalid_returns_bad_request(self):
        # Arrange
        expected: DetailError = {
            **self.expected_serializer_error_400,
            "errors": {"quantity": ["A valid integer is required."]},
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_1.id}",
            {"quantity": "f"},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(expected, actual, response, 400)

    def test_update_existing_orderline_negative_returns_bad_request(self):
        # Arrange
        expected: DetailError = {
            **self.expected_serializer_error_400,
            "errors": {
                "quantity": [
                    "Ensure this value is greater than or equal to 0."
                ]
            },
        }

        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_1.id}",
            {"quantity": -1},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(expected, actual, response, 400)

    def test_nonexistant_orderid_returns_not_found(self):
        expected = {
            **self.expected_base_404,
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
        self.assertJSONErrorResponse(expected, actual, response, 404)

    def test_nonexistant_itemid_returns_not_found(self):
        expected = {
            **self.expected_base_404,
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
        self.assertJSONErrorResponse(expected, actual, response, 404)

    def test_invalid_orderid_returns_not_found(self):

        # Act
        response = client.put(
            f"/api/orders/f/orderline/{self.test_item_2.id}",
            {},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )

    def test_invalid_itemid_returns_not_found(self):
        # Act
        response = client.put(
            f"/api/orders/{self.test_order_1.id}/orderline/f",
            {},
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )

    def test_delete_valid_returns_ok(self):
        # Arrange
        expected: OrderType = self.get_mock_order_api(
            self.test_order_1,
            self.status_pending,
            [
                self.get_mock_order_item_api(self.test_item_2, 1),
            ],
        )

        # Act
        response = client.delete(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_1.id}"
        )
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_delete_nonexistant_id_returns_not_found(self):
        expected = {
            **self.expected_base_404,
            "detail": "A server error occurred.",
            "title": "A server error occurred.",
            "type": "http://testserver/problems/error/",
        }
        # Act
        response = client.delete(
            f"/api/orders/{self.test_order_1.id}/orderline/{self.test_item_3.id}"
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(expected, actual, response, 404)
