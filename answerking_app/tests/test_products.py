from typing import Any, Dict
from typing_extensions import reveal_type
from django.core.handlers.wsgi import WSGIHandler, WSGIRequest
from django.test import Client
from assertpy import assert_that
from ddt import ddt, data

from answerking_app.tests.BaseTestClass import TestBase

client = Client()


@ddt
class GetTests(TestBase):
    def test_get_all_without_products_returns_no_content(self):
        response = client.get("/api/products")
        assert_that(response.json()).is_equal_to([])
        assert_that(response.status_code).is_equal_to(200)

    # @data("basic-3.json", "basic-1-list.json", "extreme-5.json")
    # def test_get_all_with_products_returns_ok(self, seed):
    #     seededData = self.seedFixture("product", seed)
    #     response = client.get("/api/products")
    #     assert_that(response.json()).is_equal_to(seededData)
    #     assert_that(response.status_code).is_equal_to(200)

    # def test_get_id_valid_returns_ok(self):
    #     seededData = self.seedFixture("product", "basic-1.json")
    #     response = client.get(f"/api/products/{seededData['id']}")
    #     assert_that(response.json()).is_equal_to(seededData)
    #     assert_that(response.status_code).is_equal_to(200)

    def test_get_invalid_id_returns_bad_request(self):
        response = client.get("/api/products/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_get_non_existent_id_returns_not_found(self):
        response = client.get("/api/products/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)


@ddt
class PostTests(TestBase):
    # @data(
    #     "basic-1.json",
    #     "boundry-name.json",
    #     "boundry-description.json",
    #     "boundry-price.json",
    # )
    # def test_post_valid_returns_ok(self, data):
    #     postData = self.getFixture("product", data)
    #     response = client.post(
    #         "/api/products", postData, content_type="application/json"
    #     )
    #     getResponse = client.get("/api/products")
    #     assert_that(response.json()).is_equal_to(postData)
    #     assert_that(response.status_code).is_equal_to(201)
    #     assert_that(getResponse.json()).contains(postData)

    @data(
        "invalid-id.json",
        "invalid-name.json",
        "invalid-description.json",
        "invalid-retired.json",
        "invalid-missing-fields-1.json",
        "invalid-missing-fields-2.json",
    )
    def test_post_invalid_data_returns_bad_request(self, data):
        postData = self.getFixture("product", data)
        response = client.post(
            "/api/products",
            postData,
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
        self.seedFixture("product", "basic-1.json")
        postData = self.getFixture("product", "basic-1.json")
        response = client.post(
            "/api/products", postData, content_type="application/json"
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)


@ddt
class PutTests(TestBase):
    # @data(
    #     "basic-1-update.json",
    #     "boundry-name.json",
    #     "boundry-description.json",
    #     "boundry-price.json",
    # )
    # def test_put_valid_returns_ok(self, data):
    #     seededData = self.seedFixture("product", "basic-1.json")
    #     putData = self.getFixture("product", data)
    #     response = client.put(
    #         f"/api/products/{seededData['id']}",
    #         putData,
    #         content_type="application/json",
    #     )
    #     getResponse = client.get("/api/products")
    #     assert_that(response.json()).is_equal_to(putData)
    #     assert_that(response.status_code).is_equal_to(200)
    #     assert_that(getResponse.json()).contains(putData)
    #     assert_that(getResponse.json()).does_not_contain(seededData)

    @data(
        "invalid-id.json",
        "invalid-name.json",
        "invalid-description.json",
        "invalid-retired.json",
        "invalid-missing-fields-1.json",
        "invalid-missing-fields-2.json",
    )
    def test_put_invalid_data_returns_bad_request(self, data):
        seededData = self.seedFixture("product", "basic-1.json")
        putData = self.getFixture("product", data)
        response = client.put(
            f"/api/products/{seededData['id']}",  # type: ignore[GeneralTypeIssue]
            putData,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_invalid_json_returns_bad_request(self):
        self.seedFixture("product", "basic-1.json")
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
        self.seedFixture("product", "basic-1.json")
        seededData2 = self.seedFixture(
            "product", "basic-1-different-name.json"
        )
        putData = self.getFixture("product", "basic-1-update-dup-name.json")
        response = client.put(
            f"/api/products/{seededData2['id']}",  # type: ignore[GeneralTypeIssue]
            putData,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)


class DeleteTests(TestBase):
    def test_delete_with_products_returns_ok(self):
        seededData = self.seedFixture("product", "basic-1.json")
        response = client.delete(f"/api/products/{seededData['id']}")  # type: ignore[GeneralTypeIssue]
        getResponse = client.get(f"/api/products/{seededData['id']}")  # type: ignore[GeneralTypeIssue]
        assert_that(response.status_code).is_equal_to(200)
        assert_that(str(getResponse.json())).contains("'retired': True")

    def test_delete_invalid_id_returns_bad_request(self):
        response = client.delete("/api/products/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_delete_non_existent_id_returns_not_found(self):
        response = client.delete("/api/products/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)
