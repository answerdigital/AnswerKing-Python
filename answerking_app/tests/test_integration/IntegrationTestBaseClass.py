from django.test import TransactionTestCase
from answerking_app.models.models import Product, Category, Tag

from snapshottest import TestCase
import json


class IntegrationTestBase(TransactionTestCase, TestCase):
    def preload_products(self, products_to_load: list[str]) -> None:
        for prod_json_file in products_to_load:
            self.seedFixture("products", prod_json_file)

    def seed_tag_with_prod(self, tag_json, prod_json):
        tag_id, prod_id = self._seed_x_with_y(
            "tags", tag_json, "products", prod_json
        )
        tag: Tag = Tag.objects.get(pk=tag_id)
        prod: Product = Product.objects.get(pk=prod_id)
        tag.products.add(prod)
        return tag_id, prod_id

    def seed_cat_with_prod(self, cat_json, prod_json):
        cat_id, prod_id = self._seed_x_with_y(
            "categories", cat_json, "products", prod_json
        )
        cat: Category = Category.objects.get(pk=cat_id)
        prod: Product = Product.objects.get(pk=prod_id)
        cat.product_set.add(prod)
        return cat_id, prod_id

    def _seed_x_with_y(self, x, x_json, y, y_json):
        seeded_data_x = self.seedFixture(x, x_json)
        seeded_data_y = self.seedFixture(y, y_json)
        x_id = seeded_data_x["id"]  # type: ignore[GeneralTypeIssue]
        y_id = seeded_data_y["id"]  # type: ignore[GeneralTypeIssue]
        return x_id, y_id

    def seedListFixture(self, fixture_type, list_data):
        for item in list_data:
            if fixture_type == "products":
                Product.objects.create(**item)
            elif fixture_type == "categories":
                Category.objects.create(**item)
            elif fixture_type == "tags":
                Tag.objects.create(**item)
            else:
                raise ValueError(f"Unrecognised seeding type {fixture_type}")

    def seedDictFixture(self, fixture_type, dict_data):
        if fixture_type == "products":
            Product.objects.create(**dict_data)
        elif fixture_type == "categories":
            Category.objects.create(**dict_data)
        elif fixture_type == "tags":
            Tag.objects.create(**dict_data)
        else:
            raise ValueError(f"Unrecognised seeding type {fixture_type}")

    def seedFixture(self, fixture_type, fixture_name):
        data = self.getFixture(fixture_type, fixture_name)
        if fixture_type in ["products", "categories", "tags"]:
            if isinstance(data, list):
                self.seedListFixture(fixture_type, data)
            elif isinstance(data, dict):
                self.seedDictFixture(fixture_type, data)
            else:
                raise ValueError(f"{data} is not valid json")
            return data
        else:
            raise ValueError(
                f"{fixture_type} is not a valid data seeding type"
            )

    def getFixture(self, fixture_type, fixture_name):
        fixture_path = "answerking_app/tests/test_integration/fixtures"
        return json.load(open(f"{fixture_path}/{fixture_type}/{fixture_name}"))

    def assertJSONErrorResponse(self, response):
        self.assertIsInstance(response.pop("traceId"), str)  # type: ignore[reportGeneralTypeIssues]
        self.assertMatchSnapshot(response)
