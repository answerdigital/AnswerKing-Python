from django.test import TransactionTestCase
from answerking_app.models.models import Product, Category

from snapshottest import TestCase
import json


class IntegrationTestBase(TransactionTestCase, TestCase):
    def seed_cat_with_prod(self, cat_json, prod_json):
        seeded_data_cat = self.seedFixture("categories", cat_json)
        seeded_data_prod = self.seedFixture("products", prod_json)
        cat_id = seeded_data_cat["id"]  # type: ignore[GeneralTypeIssue]
        prod_id = seeded_data_prod["id"]  # type: ignore[GeneralTypeIssue]
        cat: Category = Category.objects.get(pk=cat_id)
        prod: Product = Product.objects.get(pk=prod_id)
        cat.product_set.add(prod)
        return cat_id, prod_id

    def seedListFixture(self, fixture_type, list_data):
        for item in list_data:
            if fixture_type == "products":
                Product.objects.create(**item)
            elif fixture_type == "categories":
                Category.objects.create(**item)
            else:
                raise ValueError(f"Unrecognised seeding type {fixture_type}")

    def seedDictFixture(self, fixture_type, dict_data):
        if fixture_type == "products":
            Product.objects.create(**dict_data)
        elif fixture_type == "categories":
            Category.objects.create(**dict_data)
        else:
            raise ValueError(f"Unrecognised seeding type {fixture_type}")

    def seedFixture(self, fixture_type, fixture_name):
        data = self.getFixture(fixture_type, fixture_name)
        if fixture_type in ["products", "categories"]:
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
