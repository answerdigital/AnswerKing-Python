import json
from unittest.mock import Mock, MagicMock

from django.http import Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import ParseError
from django.db import IntegrityError
from MySQLdb.constants.ER import DUP_ENTRY

from answerking_app.models.models import Product
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase
from answerking_app.utils.mixins.ApiExceptions import ProblemDetails
from answerking_app.utils.url_parameter_check import check_url_parameter
from answerking_app.utils.get_object_or_400 import get_product_or_400
from answerking_app.utils.json404_middleware_config import json404_response
from answerking_app.utils.exceptions_handler import wrapper

from rest_framework import status
from rest_framework.response import Response


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
        self.assertEqual(check_url_parameter(10), None)

    def test_check_url_parameter_invalid_number(self):
        self.assertRaises(ProblemDetails, check_url_parameter, 0)

    def test_check_url_parameter_invalid_string(self):
        self.assertRaises(ProblemDetails, check_url_parameter, "f")

    def test_check_url_parameter_invalid_correct_exception_info(self):
        with self.assertRaises(ProblemDetails) as error:
            check_url_parameter(0)
        self.assertEqual(
            error.exception.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(error.exception.detail, "Invalid parameters")
        self.assertEqual(
            error.exception.title, "Request has invalid parameters"
        )

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

        self.assertRaises(
            ProblemDetails, get_product_or_400, Product, test_prod.pk + 1
        )

    def test_get_product_or_400_invalid_correct_exception_info(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )

        with self.assertRaises(ProblemDetails) as error:
            get_product_or_400(Product, test_prod.pk + 1)
        self.assertEqual(
            error.exception.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(error.exception.detail, "Product was not Found")
        self.assertEqual(error.exception.title, "Product not found")

    def test_exception_handler_correct_exception_info_object_does_not_exist(
        self,
    ):
        exc: Mock = Mock(spec=ObjectDoesNotExist)
        context: MagicMock = MagicMock()
        context.request = "get"

        response: Response = wrapper(exc, context)
        actual_data: dict = response.data

        self.assertEqual(actual_data["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(actual_data["detail"], "Object was not Found")
        self.assertEqual(actual_data["title"], "Resource not found")

    def test_exception_handler_correct_exception_info_http404(self):
        exc: Mock = Mock(spec=Http404)
        context: MagicMock = MagicMock()
        context.request = "get"

        response: Response = wrapper(exc, context)
        actual_data: dict = response.data

        self.assertEqual(actual_data["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(actual_data["detail"], "Not Found")
        self.assertEqual(actual_data["title"], "Resource not found")

    def test_exception_handler_correct_exception_info_validation_error(self):
        exc: Mock = Mock(spec=ValidationError)
        exc.detail = ""
        context: MagicMock = MagicMock()
        context.request = "get"

        response: Response = wrapper(exc, context)
        actual_data: dict = response.data

        self.assertEqual(actual_data["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(actual_data["detail"], "Validation Error")
        self.assertEqual(actual_data["title"], "Invalid input.")

    def test_exception_handler_correct_exception_info_parse_error(self):
        exc: Mock = Mock(spec=ParseError)
        exc.detail = ""
        context: MagicMock = MagicMock()
        context.request = "get"

        response: Response = wrapper(exc, context)
        actual_data: dict = response.data

        self.assertEqual(actual_data["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(actual_data["detail"], "Parsing JSON Error")
        self.assertEqual(actual_data["title"], "Invalid input json.")

    def test_exception_handler_correct_exception_info_integrity_error(self):
        exc: MagicMock = MagicMock(spec=IntegrityError)
        exc.args = [DUP_ENTRY]
        context: MagicMock = MagicMock()
        context.request = "get"

        response: Response = wrapper(exc, context)
        actual_data: dict = response.data

        self.assertEqual(actual_data["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(actual_data["detail"], "This name already exists")

    def test_exception_handler_correct_exception_info_integrity_error_else(
        self,
    ):
        exc: MagicMock = MagicMock(spec=IntegrityError)
        context: MagicMock = MagicMock()
        context.request = "get"

        response: Response = wrapper(exc, context)
        actual_data: dict = response.data

        self.assertEqual(
            actual_data["status"], status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_json404_response(self):
        request: Mock = Mock()
        request.scheme = "https"
        request.get_host.return_value = "127.0.0.1:8000"

        response: JsonResponse = json404_response(request)
        actual_response_content: dict = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(actual_response_content["detail"], "Not Found")
        self.assertEqual(
            actual_response_content["title"], "Resource not found"
        )
        self.assertEqual(
            actual_response_content["type"],
            "https://127.0.0.1:8000/problems/not_found/",
        )
        self.assertEqual(
            response.headers["Content-Type"], "application/problem+json"
        )
