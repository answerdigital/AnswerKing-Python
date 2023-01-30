from django.test import Client
from assertpy import assert_that
from ddt import ddt, data
from freezegun import freeze_time

from answerking_app.tests.test_integration.IntegrationTestBaseClass import IntegrationTestBase
from answerking_app.models.models import Category, Product

client = Client()
frozen_time = "2022-01-01T01:02:03.000000Z"


@ddt()
class GetTests(IntegrationTestBase):
    def seed_cat_with_prod(self, cat_json, prod_json) -> int:
        seeded_data_cat = self.seedFixture("categories", cat_json)
        seeded_data_prod = self.seedFixture("products", prod_json)
        cat = Category.objects.get(pk=seeded_data_cat['id'])
        prod = Product.objects.get(pk=seeded_data_prod['id'])
        cat.products.add(prod)
        seeded_data_cat_id: int = seeded_data_cat['id']
        return seeded_data_cat_id

    @freeze_time(frozen_time)
    def test_get_all_without_categories_returns_no_content(self):
        response = client.get("/api/categories")
        assert_that(response.json()).is_equal_to([])
        assert_that(response.status_code).is_equal_to(200)

    @freeze_time(frozen_time)
    @data("basic-3.json", "basic-1-list.json", "extreme-3.json")
    def test_get_all_with_categories_returns_ok(self, seed):
        self.seedFixture("categories", seed)
        response = client.get("/api/categories")
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    @freeze_time(frozen_time)
    def test_get_id_valid_returns_ok(self):
        seeded_data = self.seedFixture("categories", "basic-1.json")
        response = client.get(f"/api/categories/{seeded_data['id']}")
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    @freeze_time(frozen_time)
    def test_get_id_valid_with_products_returns_ok(self):
        seeded_data_cat_id = self.seed_cat_with_prod("basic-1.json", "basic-1.json")
        response = client.get(f"/api/categories/{seeded_data_cat_id}")
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    def test_get_invalid_id_returns_bad_request(self):
        response = client.get("/api/categories/invalid-id")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_get_non_existent_id_returns_not_found(self):
        response = client.get("/api/categories/1")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)

    def test_get_prods_in_cat_returns_ok(self):
        seeded_data_cat_id = self.seed_cat_with_prod("basic-1.json", "basic-1.json")
        response = client.get(f"/api/categories/{seeded_data_cat_id}/products")
        self.assertMatchSnapshot(response.json())
        assert_that(response.status_code).is_equal_to(200)

    def test_get_prods_in_cat_invalid_id_returns_bad_request(self):
        response = client.get("/api/categories/invalid-id/products")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_get_prods_in_cat_non_existent_id_returns_not_found(self):
        response = client.get("/api/categories/1/products")
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(404)


@ddt
class PostTests(IntegrationTestBase):
    def preload_products(self, products_to_load: list[str]) -> None:
        for prod_json_file in products_to_load:
            self.seedFixture("products", prod_json_file)

    @data(
        "basic-1-post.json",
        "boundary-name.json",
        "boundary-description.json",
    )
    @freeze_time(frozen_time)
    def test_post_valid_returns_ok(self, cat_data):
        post_data = self.getFixture("categories", cat_data)
        response = client.post(
            "/api/categories", post_data, content_type="application/json"
        )
        getResponse = client.get("/api/categories")
        self.assertMatchSnapshot(getResponse.json())
        assert_that(response.status_code).is_equal_to(201)

    @data("basic-1-with-products.json")
    @freeze_time(frozen_time)
    def test_post_valid_with_products_returns_ok(self, cat_data):
        post_data = self.getFixture("categories", cat_data)
        self.preload_products(["basic-3.json"])
        response = client.post(
            "/api/categories", post_data, content_type="application/json"
        )
        getResponse = client.get("/api/categories")
        self.assertMatchSnapshot(getResponse.json())
        assert_that(response.status_code).is_equal_to(201)

    @data(
        "invalid-id.json",
        "invalid-name.json",
        "invalid-description.json",
        "invalid-missing-fields.json",
    )
    def test_post_invalid_data_returns_bad_request(self, cat_data):
        post_data = self.getFixture("categories", cat_data)
        response = client.post(
            "/api/categories",
            post_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

    def test_post_invalid_json_returns_bad_request(self):
        invalid_json_data: str = '{"invalid": }'
        response = client.post(
            "/api/categories",
            invalid_json_data,
            content_type="application/json",
        )
        self.assertJSONErrorResponse(response.json())

    def test_post_duplicated_name_returns_400(self):
        self.seedFixture("categories", "basic-1.json")
        post_data = self.getFixture("categories", "basic-1-post.json")
        response = client.post(
            "/api/categories", post_data, content_type="application/json"
        )
        self.assertJSONErrorResponse(response.json())
        assert_that(response.status_code).is_equal_to(400)

@ddt()
class PutTests(IntegrationTestBase):
    @data(
        "basic-1-update.json",
        "boundary-name.json",
        "boundary-description.json",
    )
    @freeze_time(frozen_time)
    def test_put_valid_returns_ok(self, cat_data):
        seeded_data = self.seedFixture("categories", "basic-1.json")
        put_data = self.getFixture("categories", cat_data)
        response = client.put(
            f"/api/categories/{seeded_data['id']}",
            put_data,
            content_type="application/json",
        )
        getResponse = client.get("/api/categories")
        assert_that(response.status_code).is_equal_to(200)
        self.assertMatchSnapshot(getResponse.json())

    @data(
        "basic-1-update-with-products.json"
    )
    @freeze_time(frozen_time)
    def test_put_with_prods_valid_returns_ok(self, cat_update_data):
        seeded_cat_data: dict = self.seedFixture("categories", "basic-1.json")
        seeded_prod_data: list[dict] = self.seedFixture("products", "basic-3.json")
        cat: Category = Category.objects.get(pk=seeded_cat_data["id"])
        for prod_data in seeded_prod_data:
            prod: Product = Product.objects.get(pk=prod_data["id"])
            cat.products.add(prod)
        put_data = self.getFixture("categories", cat_update_data)
        response = client.put(
            f"/api/categories/{seeded_cat_data['id']}",
            put_data,
            content_type="application/json",
        )
        getResponse = client.get("/api/categories")
        assert_that(response.status_code).is_equal_to(200)
        self.assertMatchSnapshot(getResponse.json())

#
#     def test_put_invalid_id_returns_not_found(self):
#         # Act
#         response = client.get("/api/categories/f")
#         actual = response.json()
#
#         # Assert
#         self.assertJSONErrorResponse(
#             self.expected_invalid_url_parameters, actual, response, 400
#         )
#
#     def test_put_invalid_json_returns_bad_request(self):
#         # Act
#         response = client.put(
#             f"/api/categories/{self.test_cat_1.id}",
#             self.invalid_json_data,
#             content_type="application/json",
#         )
#         actual = response.json()
#
#         # Assert
#         self.assertJSONErrorResponse(
#             self.expected_base_json_parsing_error_400, actual, response, 400
#         )
#
#     def test_put_invalid_name_returns_bad_request(self):
#         # Arrange
#         invalid_post_data: CategoryType = {
#             "name": "New Name*",
#             "description": "desc",
#             "products": [],
#         }
#         expected: DetailError = {
#             **self.expected_serializer_error_400,
#             "errors": {"name": ["Enter a valid value."]},
#         }
#
#         # Act
#         response = client.put(
#             f"/api/categories/{self.test_cat_1.id}",
#             invalid_post_data,
#             content_type="application/json",
#         )
#         actual = response.json()
#
#         # Assert
#         self.assertJSONErrorResponse(expected, actual, response, 400)
#
#     def test_put_not_existing_product_returns_not_found(self):
#         # Arrange
#         product: CategoryProductType = self.invalid_mock_category_product
#         invalid_post_data: CategoryType = {
#             "name": "New Name",
#             "description": "desc",
#             "products": [product],
#         }
#         expected = {
#             **self.expected_nonexistent_product_error,
#             "type": "http://testserver/problems/error/",
#         }
#         # Act
#         response = client.put(
#             f"/api/categories/{self.test_cat_1.id}",
#             invalid_post_data,
#             content_type="application/json",
#         )
#         actual = response.json()
#
#         # Assert
#         self.assertJSONErrorResponse(expected, actual, response, 400)
#
#     def test_delete_valid_returns_ok(self):
#         # Arrange
#         expected: CategoryType = self.get_mock_category_api(
#             self.test_cat_1,
#             [
#                 self.get_mock_category_product_api(self.test_product_1),
#                 self.get_mock_category_product_api(self.test_product_2),
#             ],
#         )
#
#         expected["retired"] = True
#
#         # Act
#         response = client.delete(f"/api/categories/{self.test_cat_1.id}")
#         actual = response.json()
#
#         # Assert
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(actual, None)
#
#
#     def test_delete_invalid_id_returns_not_found(self):
#         # Act
#         response = client.delete("/api/categories/f")
#         actual = response.json()
#
#         # Assert
#         self.assertJSONErrorResponse(
#             self.expected_invalid_url_parameters, actual, response, 400
#         )
#
#     def test_put_add_duplicated_product_in_body_to_category_return_one(self):
#         # Arrange
#         product: CategoryProductType = self.get_mock_category_product_api(
#             self.test_product_1
#         )
#         post_data: CategoryType = {
#             "name": self.test_cat_2.name,
#             "description": self.test_cat_2.description,
#             "products": [product, product],
#         }
#
#         expected: CategoryType = {
#             **self.get_mock_category_api(
#                 self.test_cat_2, post_data["products"]
#             ),
#             **post_data,
#             "lastUpdated": datetime.datetime.now(),
#             "products": [product],
#         }
#
#         # Act
#         response = client.put(
#             f"/api/categories/{self.test_cat_2.id}",
#             post_data,
#             content_type="application/json",
#         )
#         actual = response.json()
#
#         self.assertUpdateTime(expected, actual, response, 200)
#
#     def test_put_duplicated_name_returns_400(self):
#         # Arrange
#         post_data: CategoryType = {
#             "name": "Vegan",
#             "description": "desc",
#             "products": [],
#         }
#
#         client.post(
#             "/api/categories", post_data, content_type="application/json"
#         )
#
#         # Act
#         response = client.put(
#             f"/api/categories/{self.test_cat_1.id + 1}",
#             post_data,
#             content_type="application/json",
#         )
#         actual = response.json()
#         # Assert
#         self.assertJSONErrorResponse(
#             self.expected_duplicated_name_error, actual, response, 400
#         )
# """
