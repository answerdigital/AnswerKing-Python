from django.db.models.query import QuerySet
from django.test import Client, TestCase, TransactionTestCase
from rest_framework.exceptions import ParseError

from answerking_app.models.models import Item
from answerking_app.utils.model_types import DetailError, ItemType

client = Client()


class ItemTests(TestCase):
    def setUp(self):
        self.test_item_1: Item = Item.objects.create(
            name="Burger",
            price=1.20,
            description="desc",
            stock=100,
            calories=100,
        )
        self.test_item_2: Item = Item.objects.create(
            name="Coke",
            price=1.50,
            description="desc",
            stock=100,
            calories=100,
        )

    def tearDown(self):
        Item.objects.all().delete()

    def test_get_all_without_items_returns_no_content(self):
        # Arrange
        Item.objects.all().delete()
        expected = []

        # Act
        response = client.get("/api/items")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_get_all_with_items_returns_ok(self):
        # Arrange
        expected: list[ItemType] = [
            {
                "id": self.test_item_1.id,
                "name": self.test_item_1.name,
                "price": f"{self.test_item_1.price:.2f}",
                "description": self.test_item_1.description,
                "stock": self.test_item_1.stock,
                "calories": self.test_item_1.calories,
                "retired": False,
            },
            {
                "id": self.test_item_2.id,
                "name": self.test_item_2.name,
                "price": f"{self.test_item_2.price:.2f}",
                "description": self.test_item_2.description,
                "stock": self.test_item_2.stock,
                "calories": self.test_item_2.calories,
                "retired": False,
            },
        ]

        # Act
        response = client.get("/api/items")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_get_id_valid_returns_ok(self):
        # Arrange
        expected: ItemType = {
            "id": self.test_item_1.id,
            "name": self.test_item_1.name,
            "price": f"{self.test_item_1.price:.2f}",
            "description": self.test_item_1.description,
            "stock": self.test_item_1.stock,
            "calories": self.test_item_1.calories,
            "retired": False,
        }

        # Act
        response = client.get(f"/api/items/{self.test_item_1.id}")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_id_returns_not_found(self):
        # Arrange
        expected: DetailError = {
            "detail": "Not Found",
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/not_found/",
        }

        # Act
        response = client.get("/api/items/f")
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_post_valid_returns_ok(self):
        # Arrange
        old_list = client.get("/api/items").json()
        post_data: ItemType = {
            "name": "Whopper",
            "price": "1.50",
            "description": "desc",
            "stock": 100,
            "calories": 100,
        }

        expected: ItemType = {
            "id": self.test_item_2.id + 1,
            **post_data,
            "retired": False,
        }

        # Act
        response = client.post(
            "/api/items", post_data, content_type="application/json"
        )
        actual = response.json()

        created_item: Item = Item.objects.filter(name="Whopper")[0]
        updated_list: QuerySet[Item] = Item.objects.all()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(created_item, updated_list)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 201)

    def test_post_invalid_json_returns_bad_request(self):
        # Arrange
        invalid_json_data: str = '{"invalid": }'
        expected: DetailError = {
            "detail": "Parsing JSON Error",
            "errors": "JSON parse error - Expecting value: line 1 column 13 (char 12)",
            "status": 400,
            "title": "Invalid input json.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/items", invalid_json_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_name_returns_bad_request(self):
        # Arrange
        invalid_post_data: ItemType = {
            "name": "Bad data£",
            "price": "1.50",
            "description": "desc",
            "stock": 100,
            "calories": 100,
        }
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {"name": ["Enter a valid value."]},
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_price_returns_bad_request(self):
        # Arrange
        invalid_post_data: ItemType = {
            "name": "Bad data",
            "price": "1.50f",
            "description": "desc",
            "stock": 100,
            "calories": 100,
        }
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {"price": ["A valid number is required."]},
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_description_returns_bad_request(self):
        # Arrange
        invalid_post_data: ItemType = {
            "name": "Bad data",
            "price": "1.50",
            "description": "desc&",
            "stock": 100,
            "calories": 100,
        }
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {"description": ["Enter a valid value."]},
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_stock_returns_bad_request(self):
        # Arrange
        invalid_post_data: ItemType = {
            "name": "Bad data",
            "price": "1.50",
            "description": "desc",
            "stock": "f100",  # type: ignore
            "calories": 100,
        }
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {"stock": ["A valid integer is required."]},
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_negative_stock_returns_bad_request(self):
        # Arrange
        invalid_post_data: ItemType = {
            "name": "Bad data",
            "price": "1.50",
            "description": "desc",
            "stock": -100,
            "calories": 100,
        }
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {
                "stock": ["Ensure this value is greater than or equal to 0."]
            },
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_calories_returns_bad_request(self):
        # Arrange
        invalid_post_data: ItemType = {
            "name": "Bad data",
            "price": "1.50",
            "description": "desc",
            "stock": 100,
            "calories": "100f",  # type: ignore
        }
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {"calories": ["A valid integer is required."]},
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_negative_calories_returns_bad_request(self):
        # Arrange
        invalid_post_data: ItemType = {
            "name": "Bad data",
            "price": "1.50",
            "description": "desc",
            "stock": 100,
            "calories": -100,
        }
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {
                "calories": [
                    "Ensure this value is greater than or equal to 0."
                ]
            },
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_put_valid_returns_ok(self):
        # Arrange
        old_item = client.get(f"/api/items/{self.test_item_1.id}").json()
        post_data: ItemType = {
            "name": "New Burger",
            "price": "1.75",
            "description": "new desc",
            "stock": 0,
            "calories": 200,
        }
        expected: ItemType = {
            "id": self.test_item_1.id,
            **post_data,
            "retired": False,
        }

        # Act
        response = client.put(
            f"/api/items/{self.test_item_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        updated_item: Item = Item.objects.filter(name="New Burger")[0]
        updated_list: QuerySet[Item] = Item.objects.all()

        # Assert
        self.assertNotEqual(old_item, actual)
        self.assertIn(updated_item, updated_list)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_put_invalid_json_returns_bad_request(self):
        # Arrange
        invalid_json_data: str = '{"invalid": }'
        expected: DetailError = {
            "detail": "Parsing JSON Error",
            "errors": "JSON parse error - Expecting value: line 1 column 13 (char 12)",
            "status": 400,
            "title": "Invalid input json.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.put(
            f"/api/items/{self.test_item_1.id}",
            invalid_json_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_put_invalid_details_returns_bad_request(self):
        # Arrange
        invalid_post_data: ItemType = {
            "name": "Bad data£",
            "price": "1.50",
            "description": "*",
            "stock": 100,
            "calories": 100,
        }
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {
                "description": ["Enter a valid value."],
                "name": ["Enter a valid value."],
            },
            "status": 400,
            "title": "Invalid input.",
            "type": "http://testserver/problems/error/",
        }

        # Act
        response = client.put(
            f"/api/items/{self.test_item_1.id}",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_delete_valid_returns_retired_true(self):
        # Arrange
        old_item: QuerySet[Item] = Item.objects.filter(pk=self.test_item_1.id)
        expected: ItemType = {
            "id": self.test_item_1.id,
            "name": self.test_item_1.name,
            "price": f"{self.test_item_1.price:.2f}",
            "description": self.test_item_1.description,
            "stock": self.test_item_1.stock,
            "calories": self.test_item_1.calories,
            "retired": True,
        }

        # Act
        response = client.delete(f"/api/items/{self.test_item_1.id}")
        items: QuerySet[Item] = Item.objects.all()
        actual = response.json()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(old_item, items)
        self.assertNotEqual(old_item, expected)
        self.assertEqual(actual, expected)

    def test_delete_invalid_id_returns_not_found(self):
        # Arrange
        expected: DetailError = {
            "detail": "Not Found",
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/not_found/",
        }

        # Act
        response = client.delete("/api/items/f")
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)


class ItemTestsDB(TransactionTestCase):
    def setUp(self):
        self.test_item_1: Item = Item.objects.create(
            name="Burger",
            price=1.20,
            description="desc",
            stock=100,
            calories=100,
        )
        self.test_item_2: Item = Item.objects.create(
            name="Coke",
            price=1.50,
            description="desc",
            stock=100,
            calories=100,
        )

    def tearDown(self):
        Item.objects.all().delete()

    def test_post_duplicated_name_returns_400(self):
        # Arrange
        post_data: ItemType = {
            "name": "Whopper",
            "price": "1.50",
            "description": "desc",
            "stock": 100,
            "calories": 100,
        }
        client.post("/api/items", post_data, content_type="application/json")

        # Act
        response = client.post(
            "/api/items", post_data, content_type="application/json"
        )

        expected: DetailError = {
            "detail": "This name already exists",
            "status": 400,
            "title": "A server error occurred.",
            "type": "http://testserver/problems/error/",
        }

        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_put_duplicated_name_returns_400(self):
        # Arrange
        old_item = client.get(f"/api/items/{self.test_item_1.id}").json()
        post_data: ItemType = {
            "name": "New Burger",
            "price": "1.75",
            "description": "new desc",
            "stock": 0,
            "calories": 200,
        }

        post_data_different_name: ItemType = {
            **post_data,
            "name": "Different Name",
        }

        client.post("/api/items", post_data, content_type="application/json")
        client.post(
            "/api/items",
            post_data_different_name,
            content_type="application/json",
        )

        # Act
        response = client.put(
            f"/api/items/{self.test_item_1.id + 1}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()
        expected: DetailError = {
            "detail": "This name already exists",
            "status": 400,
            "title": "A server error occurred.",
            "type": "http://testserver/problems/error/",
        }

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)
