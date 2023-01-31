from django.test import Client
from assertpy import assert_that
from ddt import ddt, data

from answerking_app.tests.test_integration.IntegrationTestBaseClass import (
    IntegrationTestBase,
)

client = Client()


@ddt
class GetTests(IntegrationTestBase):
    def test_get_all_without_products_returns_no_content(self):
        response = client.get("/api/products")
        assert_that(response.json()).is_equal_to([])
        assert_that(response.status_code).is_equal_to(200)

    @data("basic-3.json", "basic-1-list.json", "extreme-5.json")
    def test_get_all_with_products_returns_ok(self, seed):
        self.seedFixture("products", seed)
        response = client.get("/api/products")
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    def test_get_id_valid_returns_ok(self):
        seededData = self.seedFixture("products", "basic-1.json")
        response = client.get(f"/api/products/{seededData['id']}")  # type: ignore[GeneralTypeIssue]
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    def test_get_invalid_id_returns_bad_request(self):
        response = client.get("/api/products/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_get_non_existent_id_returns_not_found(self):
        response = client.get("/api/products/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)


@ddt
class PostTests(IntegrationTestBase):
    @data(
        "basic-1.json",
        "boundry-name.json",
        "boundry-description.json",
        "boundry-price.json",
    )
    def test_post_valid_returns_ok(self, data):
        postData = self.getFixture("products", data)
        response = client.post(
            "/api/products", postData, content_type="application/json"
        )
        getResponse = client.get("/api/products")
        self.assertMatchSnapshot(getResponse.json())
        assert_that(response.status_code).is_equal_to(201)

    @data(
        "invalid-id.json",
        "invalid-name.json",
        "invalid-description.json",
        "invalid-retired.json",
        "invalid-missing-fields-1.json",
        "invalid-missing-fields-2.json",
    )
    def test_post_invalid_data_returns_bad_request(self, data):
        post_data = self.getFixture("products", data)
        response = client.post(
            "/api/products",
            post_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_post_invalid_json_returns_bad_request(self):
        invalid_json_data: str = '{"invalid": }'
        response = client.post(
            "/api/products",
            invalid_json_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())

    def test_post_duplicated_name_returns_400(self):
        self.seedFixture("products", "basic-1.json")
        post_data = self.getFixture("products", "basic-1.json")
        response = client.post(
            "/api/products", post_data, content_type="application/json"
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)


@ddt
class PutTests(IntegrationTestBase):
    @data(
        "basic-1-update.json",
        "boundry-name.json",
        "boundry-description.json",
        "boundry-price.json",
    )
    def test_put_valid_returns_ok(self, data):
        seededData = self.seedFixture("products", "basic-1.json")
        putData = self.getFixture("products", data)
        response = client.put(
            f"/api/products/{seededData['id']}",  # type: ignore[GeneralTypeIssue]
            putData,
            content_type="application/json",
        )
        getResponse = client.get("/api/products")
        assert_that(response.status_code).is_equal_to(200)
        self.assertMatchSnapshot(getResponse.json())

    @data(
        "invalid-id.json",
        "invalid-name.json",
        "invalid-description.json",
        "invalid-retired.json",
        "invalid-missing-fields-1.json",
        "invalid-missing-fields-2.json",
    )
    def test_put_invalid_data_returns_bad_request(self, data):
        seeded_data = self.seedFixture("products", "basic-1.json")
        put_data = self.getFixture("products", data)
        response = client.put(
            f"/api/products/{seeded_data['id']}",  # type: ignore[GeneralTypeIssue]
            put_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_invalid_json_returns_bad_request(self):
        self.seedFixture("products", "basic-1.json")
        invalid_json_data: str = '{"invalid": }'
        response = client.put(
            "/api/products/1",
            invalid_json_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_invalid_id_returns_bad_request(self):
        response = client.put("/api/products/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_non_existent_id_returns_not_found(self):
        response = client.put("/api/products/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)

    def test_put_duplicated_name_returns_400(self):
        self.seedFixture("products", "basic-1.json")
        seeded_data_2 = self.seedFixture(
            "products", "basic-1-different-name.json"
        )
        put_data = self.getFixture("products", "basic-1-update-dup-name.json")
        response = client.put(
            f"/api/products/{seeded_data_2['id']}",  # type: ignore[GeneralTypeIssue]
            put_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)


class DeleteTests(IntegrationTestBase):
    def test_delete_with_products_returns_ok(self):
        seeded_data = self.seedFixture("products", "basic-1.json")
        prod_url = f"/api/products/{seeded_data['id']}"  # type: ignore[GeneralTypeIssue]
        response = client.delete(prod_url)
        get_response = client.get(prod_url)
        assert_that(response.status_code).is_equal_to(204)
        assert_that(str(get_response.json()), None)

    def test_delete_invalid_id_returns_bad_request(self):
        response = client.delete("/api/products/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_delete_non_existent_id_returns_not_found(self):
        response = client.delete("/api/products/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)

    def test_delete_already_retired_returns_gone(self):
        seeded_data = self.seedFixture("products", "basic-1.json")
        prod_url = f"/api/products/{seeded_data['id']}"  # type: ignore[GeneralTypeIssue]
        response_1 = client.delete(prod_url)
        response_2 = client.delete(prod_url)
        assert_that(response_1.status_code).is_equal_to(204)
        self.assertJSONErrorResponse(response_2.json())
        assert_that(response_2.status_code).is_equal_to(410)
