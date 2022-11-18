from django.db.models.query import QuerySet
from django.test import Client, TestCase, TransactionTestCase

from answerking_app.models.models import Category, Product
from answerking_app.tests.BaseTestClass import TestBase
from answerking_app.utils.model_types import (
    CategoryType,
    DetailError,
    ProductType,
)

client = Client()


class CategoryTests(TestBase, TestCase):
    def test_get_all_without_categories_returns_no_content(self):
        # Arrange
        Category.objects.all().delete()
        expected = []

        # Act
        response = client.get("/api/categories")
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_get_all_with_categories_returns_ok(self):
        # Arrange
        expected: list[CategoryType] = [
            self.get_mock_category_api(
                self.test_cat_1,
                [
                    self.get_mock_product_api(self.test_product_1),
                    self.get_mock_product_api(self.test_product_2),
                ],
            ),
            self.get_mock_category_api(self.test_cat_2),
        ]

        # Act
        response = client.get("/api/categories")
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_get_valid_id_returns_ok(self):
        # Arrange
        expected: CategoryType = self.get_mock_category_api(
            self.test_cat_1,
            [
                self.get_mock_product_api(self.test_product_1),
                self.get_mock_product_api(self.test_product_2),
            ],
        )

        # Act
        response = client.get(f"/api/categories/{self.test_cat_1.id}")
        actual = response.json()
        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_get_invalid_id_returns_not_found(self):
        # Act
        response = client.get("/api/categories/f")
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )

    def test_post_valid_with_products_returns_ok(self):
        # Arrange
        old_list = client.get("/api/categories").json()

        product: ProductType = self.get_mock_product_api(self.test_product_3)
        post_data: CategoryType = {"name": "Vegetarian", "products": [product]}

        expected: CategoryType = {
            **post_data,
            "id": self.test_cat_2.id + 1,
            "retired": False,
        }

        # Act
        response = client.post(
            "/api/categories", post_data, content_type="application/json"
        )
        actual = response.json()

        created_category: Category = Category.objects.filter(
            name="Vegetarian"
        )[0]
        created_category_products: list[ProductType] = actual["products"]
        updated_list: QuerySet[Category] = Category.objects.all()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(created_category, updated_list)
        self.assertIn(product, created_category_products)
        self.assertJSONResponse(expected, actual, response, 201)

    def test_post_valid_without_products_returns_ok(self):
        # Arrange
        old_list = client.get("/api/categories").json()
        post_data: CategoryType = {"name": "Gluten Free", "products": []}

        expected: CategoryType = {
            **post_data,
            "id": self.test_cat_2.id + 1,
            "retired": False,
        }

        # Act
        response = client.post(
            "/api/categories", post_data, content_type="application/json"
        )
        actual = response.json()

        created_product: Category = Category.objects.filter(
            name="Gluten Free"
        )[0]
        updated_list: QuerySet[Category] = Category.objects.all()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(created_product, updated_list)
        self.assertJSONResponse(expected, actual, response, 201)

    def test_post_invalid_json_returns_bad_request(self):
        # Act
        response = client.post(
            "/api/categories",
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
        invalid_post_data: CategoryType = {
            "name": "Vegetarian%",
            "products": [],
        }
        expected: DetailError = {**self.expected_serializer_error_400}
        expected["errors"] = {"name": ["Enter a valid value."]}

        # Act
        response = client.post(
            "/api/categories",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(expected, actual, response, 400)

    def test_put_valid_without_products_returns_no_products(self):
        # Arrange
        old_category = client.get(
            f"/api/categories/{self.test_cat_1.id}"
        ).json()

        post_data: CategoryType = {"name": "New Name"}

        expected: CategoryType = {
            **post_data,
            "id": self.test_cat_1.id,
            "products": [],
            "retired": False,
        }
        # Act
        response = client.put(
            f"/api/categories/{self.test_cat_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        updated_category: Category = Category.objects.filter(name="New Name")[
            0
        ]
        updated_list: QuerySet[Category] = Category.objects.all()

        # Assert
        self.assertNotEqual(old_category, actual)
        self.assertIn(updated_category, updated_list)
        self.assertJSONResponse(expected, actual, response, 200)

    def test_put_invalid_id_returns_not_found(self):
        # Act
        response = client.get("/api/categories/f")
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )

    def test_put_invalid_json_returns_bad_request(self):
        # Arrange
        invalid_json_data: str = '{"invalid": }'
        # Act
        response = client.put(
            f"/api/categories/{self.test_cat_1.id}",
            self.invalid_json_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_json_parsing_error_400, actual, response, 400
        )

    def test_put_invalid_name_returns_bad_request(self):
        # Arrange
        invalid_post_data: CategoryType = {
            "name": "New Name*",
            "products": [],
        }
        expected: DetailError = {
            **self.expected_serializer_error_400,
            "errors": {"name": ["Enter a valid value."]},
        }

        # Act
        response = client.put(
            f"/api/categories/{self.test_cat_1.id}",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(expected, actual, response, 400)

    def test_put_not_existing_product_returns_not_found(self):
        # Arrange
        product: ProductType = {
            **self.get_mock_product_api(self.test_product_1),
            "id": -1,
        }
        invalid_post_data: CategoryType = {
            "name": "New Name",
            "products": [product],
        }
        expected = {
            **self.expected_base_404,
            "type": "http://testserver/problems/error/",
        }
        # Act
        response = client.put(
            f"/api/categories/{self.test_cat_1.id}",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(expected, actual, response, 404)

    def test_put_wrong_product_except_id_returns_correct_product_details(self):
        # Arrange
        product_with_wrong_info: ProductType = {
            "id": self.test_product_1.id,
            "name": "Rubbish name",
            "price": "100",
            "description": "new text new text",
            "stock": 666,
            "calories": 666,
            "retired": False,
        }
        invalid_post_data: CategoryType = {
            "name": "Burgers",
            "products": [product_with_wrong_info],
        }
        expected: CategoryType = {
            "id": self.test_cat_1.id,
            "name": self.test_cat_1.name,
            "products": [self.get_mock_product_api(self.test_product_1)],
            "retired": False,
        }

        # Act
        response = client.put(
            f"/api/categories/{self.test_cat_1.id}",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertNotEqual(invalid_post_data, actual)
        self.assertJSONResponse(expected, actual, response, 200)

    def test_delete_valid_returns_ok(self):
        # Arrange
        category: Category = Category.objects.filter(pk=self.test_cat_1.id)

        # Act
        response = client.delete(f"/api/categories/{self.test_cat_1.id}")
        categories: QuerySet[Category] = Category.objects.all()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(category, categories)

    def test_delete_invalid_id_returns_not_found(self):
        # Act
        response = client.delete("/api/categories/f")
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )

    def test_put_add_duplicated_product_in_body_to_category_return_one(self):
        # Arrange
        product: ProductType = self.get_mock_product_api(self.test_product_1)
        post_data: CategoryType = self.get_mock_category_api(
            self.test_cat_1, [product, product]
        )
        expected: CategoryType = {
            **post_data,
            "products": [product],
        }
        # Act
        response = client.put(
            f"/api/categories/{self.test_cat_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()
        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_put_add_duplicated_product_in_url_to_category_return_400(self):
        # Act
        response = client.put(
            f"/api/categories/{self.test_cat_1.id}/products/{self.test_product_1.id}",
            content_type="application/json",
        )
        actual = response.json()
        # Assert
        self.assertJSONErrorResponse(
            self.expected_product_already_in_category, actual, response, 400
        )


class CategoryTestsDB(TestBase, TransactionTestCase):
    def test_post_duplicated_name_returns_400(self):
        # Arrange
        post_data: CategoryType = {"name": "Vegan", "products": []}
        client.post(
            "/api/categories", post_data, content_type="application/json"
        )

        # Act
        response = client.post(
            "/api/categories", post_data, content_type="application/json"
        )

        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_duplicated_name_error, actual, response, 400
        )

    def test_put_duplicated_name_returns_400(self):
        # Arrange
        post_data: CategoryType = {"name": "Vegan", "products": []}

        client.post(
            "/api/categories", post_data, content_type="application/json"
        )

        # Act
        response = client.put(
            f"/api/categories/{self.test_cat_1.id + 1}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()
        # Assert
        self.assertJSONErrorResponse(
            self.expected_duplicated_name_error, actual, response, 400
        )
