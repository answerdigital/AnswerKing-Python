from django.test import Client, TestCase
from assertpy import assert_that
from snapshottest import TestCase
from ddt import ddt, data

from answerking_app.tests.BaseTestClass import TestBase

client = Client()


@ddt
class GetTests(TestBase, TestCase):
    def test_get_all_without_items_returns_no_content(self):
        response = client.get("/api/items")
        assert_that(response.json()).is_equal_to([])
        assert_that(response.status_code).is_equal_to(200)

    @data("basic-3.json", "basic-1-list.json", "extreme-5.json")
    def test_get_all_with_items_returns_ok(self, seed):
        seededData = self.seedFixture("items", seed)
        response = client.get("/api/items")
        assert_that(response.json()).is_equal_to(seededData)
        assert_that(response.status_code).is_equal_to(200)

    def test_get_id_valid_returns_ok(self):
        seededData = self.seedFixture("items", "basic-1.json")
        response = client.get(f"/api/items/{seededData['id']}")
        assert_that(response.json()).is_equal_to(seededData)
        assert_that(response.status_code).is_equal_to(200)

    def test_get_invalid_id_returns_not_found(self):
        response = client.get("/api/items/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)

    def test_get_non_existent_id_returns_not_found(self):
        response = client.get("/api/items/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)


@ddt
class PostTests(TestBase, TestCase):
    @data(
        "basic-1.json",
        "boundry-name.json",
        "boundry-description.json",
        "boundry-price.json",
    )
    def test_post_valid_returns_ok(self, data):
        postData = self.getFixture("items", data)
        response = client.post(
            "/api/items", postData, content_type="application/json"
        )
        getResponse = client.get("/api/items")
        assert_that(response.json()).is_equal_to(postData)
        assert_that(response.status_code).is_equal_to(201)
        assert_that(getResponse.json()).contains(postData)

    @data(
        "invalid-id.json",
        "invalid-name.json",
        "invalid-calories.json",
        "invalid-description.json",
        "invalid-retired.json",
        "invalid-stock.json",
        "invalid-missing-fields-1.json",
        "invalid-missing-fields-2.json",
        "invalid-missing-fields-3.json",
    )
    def test_post_invalid_data_returns_bad_request(self, data):
        postData = self.getFixture("items", data)
        response = client.post(
            "/api/items",
            postData,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_post_invalid_json_returns_bad_request(self):
        invalid_json_data: str = '{"invalid": }'
        response = client.post(
            "/api/items",
            invalid_json_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())

    def test_post_duplicated_name_returns_400(self):
        self.seedFixture("items", "basic-1.json")
        postData = self.getFixture("items", "basic-1.json")
        response = client.post(
            "/api/items", postData, content_type="application/json"
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)


@ddt
class PutTests(TestBase, TestCase):
    @data(
        "basic-1-update.json",
        "boundry-name.json",
        "boundry-description.json",
        "boundry-price.json",
    )
    def test_put_valid_returns_ok(self, data):
        seededData = self.seedFixture("items", "basic-1.json")
        putData = self.getFixture("items", data)
        response = client.put(
            f"/api/items/{seededData['id']}",
            putData,
            content_type="application/json",
        )
        getResponse = client.get("/api/items")
        assert_that(response.json()).is_equal_to(putData)
        assert_that(response.status_code).is_equal_to(200)
        assert_that(getResponse.json()).contains(putData)
        assert_that(getResponse.json()).does_not_contain(seededData)

    @data(
        "invalid-id.json",
        "invalid-name.json",
        "invalid-calories.json",
        "invalid-description.json",
        "invalid-retired.json",
        "invalid-stock.json",
        "invalid-missing-fields-1.json",
        "invalid-missing-fields-2.json",
        "invalid-missing-fields-3.json",
    )
    def test_put_invalid_data_returns_bad_request(self, data):
        seededData = self.seedFixture("items", "basic-1.json")
        putData = self.getFixture("items", data)
        response = client.put(
            f"/api/items/{seededData['id']}",
            putData,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_invalid_json_returns_bad_request(self):
        invalid_json_data: str = '{"invalid": }'
        response = client.put(
            "/api/items/1",
            invalid_json_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())

    def test_put_invalid_id_returns_not_found(self):
        response = client.put("/api/items/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)

    def test_put_non_existent_id_returns_not_found(self):
        response = client.put("/api/items/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)

    def test_put_duplicated_name_returns_400(self):
        self.seedFixture("items", "basic-1.json")
        seededData2 = self.seedFixture("items", "basic-1-different-name.json")
        putData = self.getFixture("items", "basic-1-update-dup-name.json")
        response = client.put(
            f"/api/items/{seededData2['id']}",
            putData,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)


class DeleteTests(TestBase, TestCase):
    def test_delete_with_items_returns_ok(self):
        seededData = self.seedFixture("items", "basic-1.json")
        response = client.delete(f"/api/items/{seededData['id']}")
        getResponse = client.get(f"/api/items/{seededData['id']}")
        assert_that(response.status_code).is_equal_to(200)
        assert_that(str(getResponse.json())).contains("'retired': True")

    def test_delete_invalid_id_returns_not_found(self):
        response = client.delete("/api/items/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)

    def test_delete_non_existent_id_returns_not_found(self):
        response = client.delete("/api/items/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)
