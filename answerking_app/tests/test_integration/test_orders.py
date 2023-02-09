from assertpy import assert_that
from ddt import ddt, data
from django.test import Client
from freezegun import freeze_time

from answerking_app.tests.test_integration.IntegrationTestBaseClass import (
    IntegrationTestBase,
)

client = Client()
frozen_time = "2022-04-01T04:02:03.000000Z"


@ddt
class GetTests(IntegrationTestBase):
    def test_get_all_without_orders_returns_no_content(self):
        response = client.get("/api/orders")
        assert_that(response.json()).is_equal_to([])
        assert_that(response.status_code).is_equal_to(200)

    @freeze_time(frozen_time)
    def test_get_all_with_orders_returns_ok(self):
        self.preload_products(["basic-3.json"])
        self.seedFixture("orders", "basic-2.json")
        response = client.get("/api/orders")
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    @freeze_time(frozen_time)
    def test_get_id_valid_returns_ok(self):
        seeded_data = self.seedFixture("orders", "basic-1.json")
        response = client.get(f"/api/orders/{seeded_data['id']}")
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    @freeze_time(frozen_time)
    def test_get_id_with_orders_with_prod_returns_ok(self):
        self.preload_products(["basic-3.json"])
        seeded_data = self.seedFixture("orders", "basic-2.json")
        response = client.get(f"/api/orders/{seeded_data['id']}")
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    def test_get_id_invalid_returns_Invalid(self):
        response = client.get("/api/orders/f")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_get_non_existent_id_returns_not_found(self):
        response = client.get("/api/orders/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)


@ddt
class PostTests(IntegrationTestBase):
    @data("basic-1-with-products.json", "basic-2.json", "basic-3.json")
    @freeze_time(frozen_time)
    def test_post_valid_with_products_returns_ok(self, order_data):
        post_data = self.getFixture("orders", order_data)
        self.preload_products(["basic-3.json"])
        response = client.post(
            "/api/orders", post_data, content_type="application/json"
        )
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(201)

    @freeze_time(frozen_time)
    def test_post_valid_with_empty_products_returns_ok(self):
        post_data = self.getFixture("orders", "basic-1.json")
        response = client.post(
            "/api/orders", post_data, content_type="application/json"
        )
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(201)

    @data(
        "invalid-missing-quantity.json",
        "invalid-product-id.json",
        "invalid-quantity.json",
        "invalid-quantity-2.json",
    )
    def test_post_invalid_data_returns_bad_request(self, seed):
        post_data = self.getFixture("orders", seed)
        response = client.post(
            "/api/orders",
            post_data,
            content_type="application/json",
        )
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_post_invalid_json_returns_bad_request(self):
        invalid_json_data: str = '{"invalid": }'
        response = client.post(
            "/api/orders",
            invalid_json_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())

    def test_post_non_existent_product_id_returns_404(self):
        post_data = self.getFixture("orders", "non_existent-product-id.json")
        response = client.post(
            "/api/orders", post_data, content_type="application/json"
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)


@ddt
class PutTests(IntegrationTestBase):
    @data("basic-1-with-products.json", "basic-2.json", "basic-3.json")
    @freeze_time(frozen_time)
    def test_put_add_valid_products_to_order_return_ok(self, seed):
        seeded_data = self.seedFixture("orders", "basic-1.json")
        self.preload_products(["basic-3.json"])
        put_data = self.getFixture("orders", seed)
        response = client.put(
            f"/api/orders/{seeded_data['id']}",  # type: ignore[GeneralTypeIssue]
            put_data,
            content_type="application/json",
        )
        assert_that(response.status_code).is_equal_to(200)
        self.assertMatchSnapshot(response.json())


    @freeze_time(frozen_time)
    def test_put_update_quantity_to_zero_return_empty_line_items(self):
        self.preload_products(["basic-3.json"])
        seeded_data = self.seedFixture("orders", "basic-2.json")
        put_data = self.getFixture("orders", "basic-2-update.json")
        response = client.put(
            f"/api/orders/{seeded_data['id']}",  # type: ignore[GeneralTypeIssue]
            put_data,
            content_type="application/json",
        )
        assert_that(response.status_code).is_equal_to(200)
        self.assertMatchSnapshot(response.json())

    def test_put_invalid_json_returns_bad_request(self):
        self.seedFixture("orders", "basic-1.json")
        invalid_json_data: str = '{"invalid": }'
        response = client.put(
            "/api/orders/1",
            invalid_json_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_invalid_id_returns_bad_request(self):
        response = client.put("/api/orders/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_non_existent_id_returns_not_found(self):
        response = client.put("/api/orders/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)

    @data(
        "invalid-missing-quantity.json",
        "invalid-product-id.json",
        "invalid-quantity.json",
        "invalid-quantity-2.json",
    )
    def test_put_invalid_products_return_bad_request(self, seed):
        self.preload_products(["basic-3.json"])
        seeded_data = self.seedFixture("orders", "basic-2.json")
        put_data = self.getFixture("orders", seed)
        response = client.put(
            f"/api/orders/{seeded_data['id']}",
            put_data,
            content_type="application/json",
        )
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(400)

"""



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

"""
"""
    def test_delete_order_valid_returns_ok(self):
        # Arrange
        old_order_status: str = self.test_order_1.order_status
        # Act
        response = client.delete(f"/api/orders/{self.test_order_1.id}")

        # Assert
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json, None)

    def test_delete_invalid_id_returns_not_found(self):
        # Arrange
        # Act
        response = client.delete("/api/orders/f")
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_invalid_url_parameters, actual, response, 400
        )
"""
