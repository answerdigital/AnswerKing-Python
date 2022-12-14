from answerking_app.models.models import Product
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails
from answerking_app.utils.url_parameter_check import check_url_parameter
from answerking_app.utils.get_object_or_400 import get_product_or_400
from answerking_app.utils.json404_middleware_config import json404_response

from rest_framework import status


class UtilsTests(UnitTestBase):

    utb = UnitTestBase()

    test_prod_data: dict = utb.get_fixture(
        "products", "plain_burger_data.json"
    )

    def setUp(self):
        Product.objects.create(**self.test_prod_data)

    def tearDown(self):
        Product.objects.all().delete()

    def test_check_url_parameter_valid(self):
        check_url_parameter(1)

    def test_check_url_parameter_invalid_number(self):
        self.assertRaises(ProblemDetails, check_url_parameter, 0)

    def test_check_url_parameter_invalid_string(self):
        self.assertRaises(ProblemDetails, check_url_parameter, "f")

    def test_check_url_parameter_invalid_correct_exception_info(self):
        with self.assertRaises(ProblemDetails) as error:
            check_url_parameter(0)
        self.assertEqual(error.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error.exception.detail, "Invalid parameters")
        self.assertEqual(error.exception.title, "Request has invalid parameters")

    def test_get_product_or_400_returns_product(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        actual_prod = get_product_or_400(Product, test_prod.pk)
        expected_prod = test_prod

        self.assertEqual(actual_prod, expected_prod)

    def test_get_product_or_400_invalid(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )

        self.assertRaises(ProblemDetails, get_product_or_400, Product, test_prod.pk+1)

    def test_get_product_or_400_invalid_correct_exception_info(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )

        with self.assertRaises(ProblemDetails) as error:
            get_product_or_400(Product, test_prod.pk+1)
        self.assertEqual(error.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error.exception.detail, "Product was not Found")
        self.assertEqual(error.exception.title, "Product not found")

