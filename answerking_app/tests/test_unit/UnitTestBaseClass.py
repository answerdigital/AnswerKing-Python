from datetime import datetime, timedelta
import json
from django.test import TransactionTestCase
from snapshottest import TestCase

from answerking_app.models.models import Category, Product, Order, LineItem


class UnitTestBase(TransactionTestCase, TestCase):

    @staticmethod
    def input_data(model, data):
        if isinstance(data, list):
            for item in data:
                model.objects.create(**item)
        elif isinstance(data, dict):
            model.objects.create(**data)
        else:
            raise Exception(f"{data} is not valid json")
        return data

    def seedFixture(self, fixture_type: str, fixture_name: str):
        num_fixtures_seeded = 0
        data = self.get_fixture(fixture_type, fixture_name)
        if fixture_type == "products":
            self.input_data(Product, data)
        elif fixture_type == "categories":
            self.input_data(Category, data)
        else:
            raise Exception(f"{fixture_type} is not a valid data seeding type")

    def get_fixture(self, fixture_type: str, fixture_name: str):
        fixture_path = "answerking_app/tests/test_unit/fixtures"
        return json.load(open(f"{fixture_path}/{fixture_type}/{fixture_name}"))

    def seed_data(self, list_fixtures: dict):
        loaded_fixtures = []
        for fixture_name, fixture_type in list_fixtures.items():
            self.seedFixture(fixture_type, fixture_name)
            loaded_fixture = self.get_fixture(fixture_type, fixture_name)
            if isinstance(loaded_fixture, list):
                loaded_fixtures.append(*loaded_fixture)
            elif isinstance(loaded_fixture, dict):
                loaded_fixtures.append(loaded_fixture)
            else:
                raise Exception(f"{type(loaded_fixture)} for is not a valid data seeding type")
        return loaded_fixtures
