from assertpy import assert_that
from ddt import data, ddt
from django.test import Client

from answerking_app.models.models import Product, Tag
from answerking_app.tests.test_integration.IntegrationTestBaseClass import \
    IntegrationTestBase

client = Client()


@ddt()
class GetTests(IntegrationTestBase):
    def test_get_all_without_tags_returns_no_content(self):
        response = client.get("/api/tags")
        assert_that(response.json()).is_equal_to([])
        assert_that(response.status_code).is_equal_to(200)

    @data("basic-3.json", "basic-1-list.json", "extreme-3.json")
    def test_get_all_with_tags_returns_ok(self, seed):
        self.seedFixture("tags", seed)
        response = client.get("/api/tags")
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    def test_get_id_valid_returns_ok(self):
        seeded_data = self.seedFixture("tags", "basic-1.json")
        response = client.get(
            f"/api/tags/{seeded_data['id']}"  # type: ignore[GeneralTypeIssue]
        )
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    def test_get_id_valid_with_products_returns_ok(self):
        seeded_data_tag_id, _ = self.seed_tag_with_prod(
            "basic-1.json", "basic-1.json"
        )
        response = client.get(f"/api/tags/{seeded_data_tag_id}")
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    def test_get_invalid_id_returns_bad_request(self):
        response = client.get("/api/tags/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_get_non_existent_id_returns_not_found(self):
        response = client.get("/api/tags/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)


@ddt
class PostTests(IntegrationTestBase):
    @data(
        "basic-1-post.json",
        "boundary-name.json",
        "boundary-description.json",
    )
    def test_post_valid_returns_ok(self, tag_data):
        post_data = self.getFixture("tags", tag_data)
        response = client.post(
            "/api/tags", post_data, content_type="application/json"
        )
        get_response = client.get("/api/tags")
        self.assertMatchSnapshot(get_response.json())
        assert_that(response.status_code).is_equal_to(201)

    @data("basic-1-with-products.json")
    def test_post_valid_with_products_returns_ok(self, tag_data):
        post_data = self.getFixture("tags", tag_data)
        self.preload_products(["basic-3.json"])
        response = client.post(
            "/api/tags", post_data, content_type="application/json"
        )
        get_response = client.get("/api/tags")
        self.assertMatchSnapshot(get_response.json())
        assert_that(response.status_code).is_equal_to(201)

    @data(
        "invalid-id.json",
        "invalid-name.json",
        "invalid-description.json",
        "invalid-missing-fields.json",
        "invalid-retired.json",
    )
    def test_post_invalid_data_returns_bad_request(self, tag_data):
        post_data = self.getFixture("tags", tag_data)
        response = client.post(
            "/api/tags",
            post_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    @data("invalid-product-id.json")
    def test_post_invalid_product_id_returns_bad_request(self, tag_data):
        post_data = self.getFixture("tags", tag_data)
        response = client.post(
            "/api/tags", post_data, content_type="application/json"
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    @data("basic-1-with-products.json")
    def test_post_nonexistent_product_id_returns_not_found(self, tag_data):
        post_data = self.getFixture("tags", tag_data)
        response = client.post(
            "/api/tags", post_data, content_type="application/json"
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_post_invalid_json_returns_bad_request(self):
        invalid_json_data: str = '{"invalid": }'
        response = client.post(
            "/api/tags",
            invalid_json_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())

    def test_post_duplicated_name_returns_400(self):
        self.seedFixture("tags", "basic-1.json")
        post_data = self.getFixture("tags", "basic-1-post.json")
        response = client.post(
            "/api/tags", post_data, content_type="application/json"
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)


@ddt
class PutTests(IntegrationTestBase):
    @data(
        "basic-1-update.json",
        "boundary-name.json",
        "boundary-description.json",
    )
    def test_put_valid_returns_ok(self, tag_data):
        seeded_data = self.seedFixture("tags", "basic-1.json")
        put_data = self.getFixture("tags", tag_data)
        response = client.put(
            f"/api/tags/{seeded_data['id']}",  # type: ignore[GeneralTypeIssue]
            put_data,
            content_type="application/json",
        )
        get_response = client.get("/api/tags")
        assert_that(response.status_code).is_equal_to(200)
        self.assertMatchSnapshot(get_response.json())

    @data("basic-1-update-with-products.json")
    def test_put_with_prods_valid_returns_ok(self, tag_update_data):
        seeded_tag_data = self.seedFixture("tags", "basic-1.json")
        seeded_prod_data = self.seedFixture("products", "basic-3.json")
        tag: Tag = Tag.objects.get(
            pk=seeded_tag_data["id"]  # type: ignore[GeneralTypeIssue]
        )
        for prod_data in seeded_prod_data:
            prod: Product = Product.objects.get(pk=prod_data["id"])
            tag.products.add(prod)
        put_data = self.getFixture("tags", tag_update_data)
        response = client.put(
            f"/api/tags/{seeded_tag_data['id']}",  # type: ignore[GeneralTypeIssue]
            put_data,
            content_type="application/json",
        )
        get_response = client.get("/api/tags")
        assert_that(response.status_code).is_equal_to(200)
        self.assertMatchSnapshot(get_response.json())

    @data(
        "invalid-id.json",
        "invalid-name.json",
        "invalid-description.json",
        "invalid-missing-fields.json",
    )
    def test_put_invalid_data_returns_bad_request(self, tag_data):
        seeded_tag_data = self.seedFixture("tags", "basic-1.json")
        put_data = self.getFixture("tags", tag_data)
        response = client.put(
            f"/api/tags/{seeded_tag_data['id']}",  # type: ignore[GeneralTypeIssue]
            put_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    @data("basic-1-update-with-products.json", "invalid-product-id.json")
    def test_put_invalid_prod_data_returns_bad_request(self, tag_update_data):
        seeded_tag_data = self.seedFixture("tags", "basic-1.json")
        seeded_prod_data = self.seedFixture("products", "basic-3.json")
        Product.objects.get(pk=3).delete()
        tag: Tag = Tag.objects.get(
            pk=seeded_tag_data["id"]  # type: ignore[GeneralTypeIssue]
        )
        for prod_data in seeded_prod_data[:2]:
            prod: Product = Product.objects.get(pk=prod_data["id"])
            tag.products.add(prod)
        put_data = self.getFixture("tags", tag_update_data)
        response = client.put(
            f"/api/tags/{seeded_tag_data['id']}",  # type: ignore[GeneralTypeIssue]
            put_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_invalid_json_returns_bad_request(self):
        self.seedFixture("tags", "basic-1.json")
        invalid_json_data: str = '{"invalid": }'
        response = client.put(
            "/api/tags/1",
            invalid_json_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_invalid_id_returns_bad_request(self):
        response = client.put("/api/tags/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_non_existent_id_returns_not_found(self):
        response = client.put("/api/tags/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)

    def test_put_duplicated_name_returns_400(self):
        self.seedFixture("tags", "basic-1.json")
        seeded_data_2 = self.seedFixture("tags", "basic-1-different-name.json")
        put_data = self.getFixture("tags", "basic-1-update-dup-name.json")
        response = client.put(
            f"/api/tags/{seeded_data_2['id']}",  # type: ignore[GeneralTypeIssue]
            put_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_put_retired_returns_gone(self):
        seeded_data = self.seedFixture("tags", "retired.json")
        put_data = self.getFixture("tags", "basic-1.json")
        response = client.put(
            f"/api/tags/{seeded_data['id']}",  # type: ignore[GeneralTypeIssue]
            put_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(410)


class DeleteTests(IntegrationTestBase):
    def test_delete_returns_ok(self):
        seeded_data = self.seedFixture("tags", "basic-1.json")
        cat_url = f"/api/tags/{seeded_data['id']}"  # type: ignore[GeneralTypeIssue]
        response = client.delete(cat_url)
        get_response = client.get(cat_url)
        assert_that(response.status_code).is_equal_to(204)
        assert_that(str(get_response.json()), None)

    def test_delete_invalid_id_returns_bad_request(self):
        response = client.delete("/api/tags/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_delete_non_existent_id_returns_not_found(self):
        response = client.delete("/api/tags/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)

    def test_delete_already_retired_returns_gone(self):
        seeded_data = self.seedFixture("tags", "basic-1.json")
        tag_url = f"/api/tags/{seeded_data['id']}"  # type: ignore[GeneralTypeIssue]
        response_1 = client.delete(tag_url)
        response_2 = client.delete(tag_url)
        assert_that(response_1.status_code).is_equal_to(204)
        self.assertJSONErrorResponse(response_2.json())
        assert_that(response_2.status_code).is_equal_to(410)
