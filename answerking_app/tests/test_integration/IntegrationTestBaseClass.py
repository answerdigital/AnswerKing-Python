from django.test import TransactionTestCase
from answerking_app.models.models import Product, Category

from snapshottest import TestCase
import json


class IntegrationTestBase(TransactionTestCase, TestCase):
    def seedFixture(self, fixture_type, fixture_name):
        data = self.getFixture(fixture_type, fixture_name)
        if fixture_type in ["products", "categories"]:
            if isinstance(data, list):
                for item in data:
                    if fixture_type == "products":
                        Product.objects.create(**item)
                    elif fixture_type == "categories":
                        Category.objects.create(**item)
                    else:
                        raise Exception(f"Unrecognised seeding type {fixture_type}")
            elif isinstance(data, dict):
                if fixture_type == "products":
                    Product.objects.create(**data)
                elif fixture_type == "categories":
                    Category.objects.create(**data)
                else:
                    raise Exception(f"Unrecognised seeding type {fixture_type}")
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
