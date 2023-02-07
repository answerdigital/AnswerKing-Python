from enum import auto
from unittest import mock

from ddt import data, ddt
from rest_framework.request import Request

from answerking_app.models.models import Category, Product, Tag
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails
from answerking_app.utils.mixins.RetireMixin import RetireMixin


@ddt
class RetireMixinUnitTests(UnitTestBase):
    cat_data = {"burgers_cat_data.json": "categories"}
    retired_cat_data = {"retired_cat_data.json": "categories"}
    product_data = {"margarita_pizza_data.json": "products"}
    retired_product_data = {"retired_product_data.json": "products"}
    tag_data = {"halal_tag_data.json": "tags"}
    retired_tag_data = {"retired_tag.json": "tags"}

    @data(retired_product_data, retired_tag_data, retired_cat_data)
    def test_update_mixin_retired_object(self, obj_data):
        model = self.seed_data_and_get_models(obj_data)[0]
        with mock.patch.object(
            RetireMixin,
            "get_object",
            create=True,
            return_value=model,
        ):
            with self.assertRaises(ProblemDetails) as context:
                RetireMixin().update(Request)
            self.assertEqual(context.exception.status_code, 410)

    @data(product_data, tag_data, cat_data)
    def test_update_mixin(self, obj_data):
        model = self.seed_data_and_get_models(obj_data)[0]
        with mock.patch.object(
            RetireMixin,
            "get_object",
            create=True,
            return_value=model,
        ):
            with mock.patch("builtins.super") as super_obj:
                RetireMixin().update(Request)
                super_obj.assert_called()
