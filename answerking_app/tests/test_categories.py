from django.db.models.query import QuerySet
from django.test import Client, TestCase, TransactionTestCase

from answerking_app.models.models import Category, Item
from answerking_app.utils.model_types import (CategoryType, DetailError,
                                              ItemType)

client = Client()


class CategoryTests(TestCase):
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
        self.test_item_3: Item = Item.objects.create(
            name="Chips",
            price=1.50,
            description="desc",
            stock=100,
            calories=100,
        )

        self.test_cat_1: Category = Category.objects.create(name="Burgers")
        self.test_cat_2: Category = Category.objects.create(name="Sides")

        self.test_cat_1.items.add(self.test_item_1)
        self.test_cat_1.items.add(self.test_item_2)

    def tearDown(self):
        Item.objects.all().delete()
        Category.objects.all().delete()

    def test_get_all_without_categories_returns_no_content(self):
        # Arrange
        Category.objects.all().delete()
        expected = []

        # Act
        response = client.get("/api/categories")
        actual = response.json()

        # Assert
        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_get_all_with_categories_returns_ok(self):
        # Arrange
        expected: list[CategoryType] = [
            {
                "id": self.test_cat_1.id,
                "name": self.test_cat_1.name,
                "items": [
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
                ],
                "retired": False,
            },
            {
                "id": self.test_cat_2.id,
                "name": self.test_cat_2.name,
                "items": [],
                "retired": False,
            },
        ]

        # Act
        response = client.get("/api/categories")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_get_valid_id_returns_ok(self):
        # Arrange
        expected: CategoryType = {
            "id": self.test_cat_1.id,
            "name": self.test_cat_1.name,
            "items": [
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
            ],
            "retired": False,
        }

        # Act
        response = client.get(f"/api/categories/{self.test_cat_1.id}")
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
        response = client.get("/api/categories/f")
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_post_valid_with_items_returns_ok(self):
        # Arrange
        old_list = client.get("/api/categories").json()

        item: ItemType = {
            "id": self.test_item_3.id,
            "name": self.test_item_3.name,
            "price": f"{self.test_item_3.price:.2f}",
            "description": self.test_item_3.description,
            "stock": self.test_item_3.stock,
            "calories": self.test_item_3.calories,
            "retired": False,
        }
        post_data: CategoryType = {"name": "Vegetarian", "items": [item]}

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
        created_category_items: list[ItemType] = actual["items"]
        updated_list: QuerySet[Category] = Category.objects.all()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(created_category, updated_list)
        self.assertIn(item, created_category_items)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 201)

    def test_post_valid_without_items_returns_ok(self):
        # Arrange
        old_list = client.get("/api/categories").json()
        post_data: CategoryType = {"name": "Gluten Free", "items": []}

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

        created_item: Category = Category.objects.filter(name="Gluten Free")[0]
        updated_list: QuerySet[Category] = Category.objects.all()

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
            "/api/categories",
            invalid_json_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_details_returns_bad_request(self):
        # Arrange
        invalid_post_data: CategoryType = {
            "name": "Vegetarian%",
            "items": [],
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
            "/api/categories",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_put_valid_without_items_returns_no_items(self):
        # Arrange
        old_category = client.get(
            f"/api/categories/{self.test_cat_1.id}"
        ).json()

        post_data: CategoryType = {"name": "New Name"}

        expected: CategoryType = {
            **post_data,
            "id": self.test_cat_1.id,
            "items": [],
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
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_put_invalid_id_returns_not_found(self):
        # Arrange
        expected: DetailError = {
            "detail": "Not Found",
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/not_found/",
        }

        # Act
        response = client.get("/api/categories/f")
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

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
            f"/api/categories/{self.test_cat_1.id}",
            invalid_json_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_put_invalid_name_returns_bad_request(self):
        # Arrange
        invalid_post_data: CategoryType = {
            "name": "New Name*",
            "items": [],
        }
        expected: DetailError = {
            "detail": "Validation Error",
            "errors": {"name": ["Enter a valid value."]},
            "status": 400,
            "title": "Invalid input.",
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
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 400)

    def test_put_not_existing_item_returns_not_found(self):
        # Arrange
        item: ItemType = {
            "id": -1,
            "name": self.test_item_1.name,
            "price": f"{self.test_item_1.price:.2f}",
            "description": self.test_item_1.description,
            "stock": self.test_item_1.stock,
            "calories": self.test_item_1.calories,
            "retired": False,
        }
        invalid_post_data: CategoryType = {
            "name": "New Name",
            "items": [item],
        }
        expected: DetailError = {
            "detail": "Object was not Found",
            "errors": ["Item matching query does not exist."],
            "status": 404,
            "title": "Resource not found",
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
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_put_wrong_item_except_id_returns_correct_item_details(self):
        # Arrange
        item_with_wrong_info: ItemType = {
            "id": self.test_item_1.id,
            "name": "Rubbish name",
            "price": "100",
            "description": "new text new text",
            "stock": 666,
            "calories": 666,
            "retired": False,
        }
        invalid_post_data: CategoryType = {
            "name": "Burgers",
            "items": [item_with_wrong_info],
        }
        expected: CategoryType = {
            "id": self.test_cat_1.id,
            "name": self.test_cat_1.name,
            "items": [
                {
                    "id": self.test_item_1.id,
                    "name": self.test_item_1.name,
                    "price": f"{self.test_item_1.price:.2f}",
                    "description": self.test_item_1.description,
                    "stock": self.test_item_1.stock,
                    "calories": self.test_item_1.calories,
                    "retired": False,
                }
            ],
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
        self.assertEqual(expected, actual)
        self.assertNotEqual(invalid_post_data, actual)
        self.assertEqual(response.status_code, 200)

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
        # Arrange
        expected: DetailError = {
            "detail": "Not Found",
            "status": 404,
            "title": "Resource not found",
            "type": "http://testserver/problems/not_found/",
        }
        # Act
        response = client.delete("/api/categories/f")
        actual = response.json()

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_put_add_duplicated_item_in_body_to_category_return_one(self):
        # Arrange
        item: ItemType = {
            "id": self.test_item_1.id,
            "name": self.test_item_1.name,
            "price": f"{self.test_item_1.price:.2f}",
            "description": self.test_item_1.description,
            "stock": self.test_item_1.stock,
            "calories": self.test_item_1.calories,
            "retired": False,
        }
        post_data: CategoryType = {
            "id": self.test_cat_1.id,
            "name": "Burgers",
            "items": [item, item],
            "retired": False,
        }
        expected: CategoryType = {
            "id": self.test_cat_1.id,
            "name": "Burgers",
            "items": [item],
            "retired": False,
        }
        # Act
        response = client.put(
            f"/api/categories/{self.test_cat_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(actual, expected)
        self.assertNotEqual(actual, post_data)

    def test_put_add_duplicated_item_in_url_to_category_return_400(self):
        # Act
        response = client.put(
            f"/api/categories/{self.test_cat_1.id}/items/{self.test_item_1.id}",
            content_type="application/json",
        )
        actual = response.json()
        expected: DetailError = {
            "detail": "A server error occurred.",
            "status": 400,
            "title": "A server error occurred.",
            "type": "http://testserver/problems/error/",
        }

        # Assert
        self.assertIsInstance(actual.pop("traceId"), str)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(actual, expected)


class CategoryTestsDB(TransactionTestCase):
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
        self.test_item_3: Item = Item.objects.create(
            name="Chips",
            price=1.50,
            description="desc",
            stock=100,
            calories=100,
        )

        self.test_cat_1: Category = Category.objects.create(name="Burgers")
        self.test_cat_2: Category = Category.objects.create(name="Sides")

        self.test_cat_1.items.add(self.test_item_1)
        self.test_cat_1.items.add(self.test_item_2)

    def tearDown(self):
        Item.objects.all().delete()
        Category.objects.all().delete()

    def test_post_duplicated_name_returns_400(self):
        # Arrange
        post_data: CategoryType = {"name": "Vegan", "items": []}
        client.post(
            "/api/categories", post_data, content_type="application/json"
        )

        # Act
        response = client.post(
            "/api/categories", post_data, content_type="application/json"
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
        post_data: CategoryType = {"name": "Vegan", "items": []}

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
