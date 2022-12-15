import json
from unittest.mock import Mock, MagicMock
import copy
from answerking_app.utils.serializer_data_functions import products_check
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
from answerking_app.utils.json404_middleware_config import json404_response
from answerking_app.utils.exceptions_handler import wrapper
from rest_framework import status
from rest_framework.response import Response


class UtilsTests(UnitTestBase):

    utb = UnitTestBase()

    test_prod_data: dict = utb.get_fixture(
        "products", "plain_burger_data.json"
    )
    test_cat_det_serializer_data: dict = utb.get_fixture(
        "categories", "cat_with_id_data.json"
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

    def test_get_product_check_product(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        data = {'products': [{'id': test_prod.id}]}
        actual_prod = products_check(data)
        expected_prod = test_prod

        self.assertEqual(actual_prod, [expected_prod])

    def test_product_check_invalid(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )

        self.assertRaises(
            ProblemDetails, products_check, {'products': [{'id': test_prod.id + 1}]}
        )

    def test_get_product_check_invalid_correct_exception_info(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
        data = {'products': [{'id': test_prod.id + 1}]}

        with self.assertRaises(ProblemDetails) as error:
            products_check(data)
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
            response.headers["Content-Type"], "application/problem+json")

    def test_products_check_return_empty_list_when_products_not_in_validated_data_pass(
        self,
    ):
        validated_data: dict = self.test_cat_det_serializer_data
        expected = []
        actual: list[Product] = products_check(validated_data)

        self.assertEqual(actual, expected)

    def test_products_check_only_needs_product_ids_pass(self):
        to_seed: dict = {
            "margarita_pizza_data.json": "products",
            "pepperoni_pizza_data.json": "products",
        }
        self.seed_data(to_seed)
        prod_1: Product = Product.objects.get(name="Margarita pizza")
        prod_2: Product = Product.objects.get(name="Pepperoni pizza")
        validated_data: dict = {
            "products": [
                {"id": prod_1.id},
                {"id": prod_2.id},
            ]
        }
        expected: list[Product] = [prod_1, prod_2]
        actual: list[Product] = products_check(validated_data)

        self.assertEqual(actual, expected)

    def test_products_check_retired_product_fail(self):
        to_seed: dict = {"retired_product_data.json": "products"}
        seeded_data: list[dict] = self.seed_data(to_seed)
        with self.assertRaises(ProblemDetails) as context:
            product_data: dict = seeded_data[0]
            product_data["id"] = Product.objects.get(name="Old Pizza").id
            validated_data: dict = copy.deepcopy(
                self.test_cat_det_serializer_data
            )
            validated_data["products"] = [product_data]
            products_check(validated_data)

        self.assertRaises(ProblemDetails)
        self.assertEqual(context.exception.status_code, status.HTTP_410_GONE)
        self.assertEqual(
            context.exception.detail, "This product has been retired"
        )
