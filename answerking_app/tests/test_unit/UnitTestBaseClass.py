import json

from django.test import TransactionTestCase
from snapshottest import TestCase

from answerking_app.models.models import Category, Product, Tag


class UnitTestBase(TransactionTestCase, TestCase):
    @staticmethod
    def input_data(model, data):
        if isinstance(data, list):
            for item in data:
                model.objects.create(**item)
        elif isinstance(data, dict):
            model.objects.create(**data)
        else:
            raise ValueError(f"{data} is not valid json")
        return data

    @staticmethod
    def get_object(model_type: str, data: dict) -> Product | Category | Tag:
        if model_type == "products":
            return Product.objects.get(**data)
        elif model_type == "categories":
            return Category.objects.get(**data)
        elif model_type == "tags":
            return Tag.objects.get(**data)
        else:
            raise ValueError(f"{model_type} is not a valid model type")

    def seedFixture(self, fixture_type: str, fixture_name: str):
        data = self.get_fixture(fixture_type, fixture_name)
        if fixture_type == "products":
            return self.input_data(Product, data)
        elif fixture_type == "categories":
            return self.input_data(Category, data)
        elif fixture_type == "tags":
            return self.input_data(Tag, data)
        else:
            raise ValueError(
                f"{fixture_type} is not a valid data seeding type"
            )

    def get_fixture(
        self,
        fixture_type: str,
        fixture_name: str,
        fixture_path="answerking_app/tests/test_unit/fixtures",
    ):
        return json.load(open(f"{fixture_path}/{fixture_type}/{fixture_name}"))

    def seed_data(self, fixtures: dict) -> list[dict]:
        loaded_fixtures = []
        for fixture_name, fixture_type in fixtures.items():
            data = self.seedFixture(fixture_type, fixture_name)
            if isinstance(data, list):
                loaded_fixtures.append(*data)
            elif isinstance(data, dict):
                loaded_fixtures.append(data)
            else:
                raise TypeError(
                    f"The type of {data} : [{type(data)}] is not valid"
                )
        return loaded_fixtures

    def seed_data_and_get_models(
        self, fixtures: dict
    ) -> list[Category | Tag | Product]:
        models: list[Category | Tag | Product] = []
        for fixture_name, fixture_type in fixtures.items():
            data = self.seedFixture(fixture_type, fixture_name)
            if isinstance(data, list):
                for i in data:
                    models.append(self.get_object(fixture_type, i))
            elif isinstance(data, dict):
                models.append(self.get_object(fixture_type, data))
            else:
                raise TypeError(
                    f"The type of {data} : [{type(data)}] is not valid"
                )
        return models
