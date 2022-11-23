from django.db.models.query import QuerySet
from django.test import Client, TestCase, TransactionTestCase

from answerking_app.models.models import Product
from answerking_app.tests.BaseTestClass import TestBase
from answerking_app.utils.model_types import DetailError, ProductType

client = Client()


class ProductTests(TestBase, TestCase):
    def test_get_all_without_products_returns_no_content(self):
        # Arrange
        Product.objects.all().delete()
        expected: list = []

        # Act
        response = client.get("/api/products")
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_get_all_with_products_returns_ok(self):
        # Arrange
        expected: list[ProductType] = [
            self.get_mock_product_api(self.test_product_1),
            self.get_mock_product_api(self.test_product_2),
            self.get_mock_product_api(self.test_product_3),
        ]

        # Act
        response = client.get("/api/products")
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_get_id_valid_returns_ok(self):
        # Arrange
        expected: ProductType = self.get_mock_product_api(self.test_product_1)

        # Act
        response = client.get(f"/api/products/{self.test_product_1.id}")
        actual = response.json()

        # Assert
        self.assertJSONResponse(expected, actual, response, 200)

    def test_get_invalid_id_returns_not_found(self):
        # Act
        response = client.get("/api/products/f")
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )

    def test_post_valid_returns_ok(self):
        # Arrange
        old_list = client.get("/api/products").json()

        expected: ProductType = {
            "id": self.test_product_3.id + 1,
            **self.post_mock_product,
            "categories": [],
            "retired": False,
        }

        # Act
        response = client.post(
            "/api/products",
            self.post_mock_product,
            content_type="application/json",
        )
        actual = response.json()

        created_product: Product = Product.objects.filter(name="Whopper")[0]
        updated_list: QuerySet[Product] = Product.objects.all()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(created_product, updated_list)
        self.assertJSONResponse(expected, actual, response, 201)

    def test_post_invalid_json_returns_bad_request(self):
        response = client.post(
            "/api/products",
            self.invalid_json_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_json_parsing_error_400, actual, response, 400
        )

    def test_post_invalid_data_returns_bad_request(self):
        error_codes_invalid_string: dict[str, list[str]] = {
            "name": ["Enter a valid value."],
            "price": ["A valid number is required."],
            "description": ["Enter a valid value."],
            "stock": ["A valid integer is required."],
            "calories": ["A valid integer is required."],
        }
        error_codes_negative_number: dict[str, list[str]] = {
            **error_codes_invalid_string,
            "price": ["Ensure this value is greater than or equal to 0."],
            "stock": ["Ensure this value is greater than or equal to 0."],
            "calories": ["Ensure this value is greater than or equal to 0."],
        }
        # Arrange
        for key in self.post_mock_product:
            for invalid_data, error_codes in [
                ("Bad data£", error_codes_invalid_string),
                (-9999, error_codes_negative_number),
            ]:
                invalid_post_data: ProductType = {**self.post_mock_product}
                invalid_post_data[key] = invalid_data
                expected: DetailError = {**self.expected_serializer_error_400}
                expected["errors"] = {key: error_codes[key]}

                # Act
                response = client.post(
                    "/api/products",
                    invalid_post_data,
                    content_type="application/json",
                )
                actual = response.json()

                # Assert
                self.assertJSONErrorResponse(expected, actual, response, 400)

    def test_put_valid_returns_ok(self):
        # Arrange
        old_product = client.get(
            f"/api/products/{self.test_product_3.id}"
        ).json()

        expected: ProductType = {
            "id": self.test_product_3.id,
            **self.post_mock_product,
            "categories": self.get_mock_product_categories(
                self.test_product_3
            ),
            "retired": False,
        }

        # Act
        response = client.put(
            f"/api/products/{self.test_product_3.id}",
            self.post_mock_product,
            content_type="application/json",
        )
        actual = response.json()

        updated_product: Product = Product.objects.filter(name="Whopper")[0]
        updated_list: QuerySet[Product] = Product.objects.all()

        # Assert
        self.assertNotEqual(old_product, actual)
        self.assertIn(updated_product, updated_list)
        self.assertJSONResponse(expected, actual, response, 200)

    def test_put_invalid_json_returns_bad_request(self):
        # Act
        response = client.put(
            f"/api/products/{self.test_product_1.id}",
            self.invalid_json_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_json_parsing_error_400, actual, response, 400
        )

    def test_delete_valid_returns_retired_true(self):
        # Arrange
        old_product: QuerySet[Product] = Product.objects.filter(
            pk=self.test_product_3.id
        )
        expected: ProductType = self.get_mock_product_api(self.test_product_3)
        expected["retired"] = True
        # Act
        response = client.delete(f"/api/products/{self.test_product_3.id}")
        products: QuerySet[Product] = Product.objects.all()
        actual = response.json()

        # Assert
        self.assertNotIn(old_product, products)
        self.assertNotEqual(old_product, expected)
        self.assertJSONResponse(actual, expected, response, 200)

    def test_delete_invalid_id_returns_not_found(self):
        # Act
        response = client.delete("/api/products/f")
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_base_404, actual, response, 404
        )


class ProductTestsDB(TestBase, TransactionTestCase):
    def test_post_duplicated_name_returns_400(self):
        # Arrange
        client.post(
            "/api/products",
            self.post_mock_product,
            content_type="application/json",
        )

        # Act
        response = client.post(
            "/api/products",
            self.post_mock_product,
            content_type="application/json",
        )

        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_duplicated_name_error, actual, response, 400
        )

    def test_put_duplicated_name_returns_400(self):
        # Arrange

        post_data_different_name: ProductType = {
            **self.post_mock_product,
            "name": "Different Name",
        }

        client.post(
            "/api/products",
            self.post_mock_product,
            content_type="application/json",
        )
        client.post(
            "/api/products",
            post_data_different_name,
            content_type="application/json",
        )

        # Act
        response = client.put(
            f"/api/products/{self.test_product_1.id + 1}",
            self.post_mock_product,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertJSONErrorResponse(
            self.expected_duplicated_name_error, actual, response, 400
        )
