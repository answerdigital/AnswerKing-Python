from django.test import TransactionTestCase
from answerking_app.models.models import Product

from snapshottest import TestCase
import json


class IntegrationTestBase(TransactionTestCase, TestCase):

    def seedFixture(self, type, fixtureName):
        data = self.getFixture(type, fixtureName)
        if type in ["products", "categories"]:
            if isinstance(data, list):
                for item in data:
                    if type == "products":
                        Product.objects.create(**item)
                    elif type == "categories":
                        Category. objects.create(**item)
                    else:
                        raise Exception(f"Unrecognised seeding type {type}")
            elif isinstance(data, dict):
                if type == "products":
                    Product.objects.create(**data)
                elif type == "categories":
                    Category.objects.create(**data)
                else:
                    raise Exception(f"Unrecognised seeding type {type}")
            else:
                raise ValueError(f"{data} is not valid json")
            return data
        else:
            raise ValueError(
                f"{fixture_type} is not a valid data seeding type"
            )

    def getFixture(self, fixture_type, fixture_name):
        fixture_path = "answerking_app/tests/fixtures"
        return json.load(open(f"{fixture_path}/{fixture_type}/{fixture_name}"))

    def assertJSONErrorResponse(self, response):
        self.assertIsInstance(response.pop("traceId"), str)  # type: ignore[reportGeneralTypeIssues]
        self.assertMatchSnapshot(response)

    # expected_serializer_error_400: DetailError = {
    #     "detail": "Validation Error",
    #     "errors": {},
    #     "status": 400,
    #     "title": "Invalid input.",
    #     "type": "http://testserver/problems/error/",
    # }
    # expected_base_json_parsing_error_400: DetailError = {
    #     "detail": "Parsing JSON Error",
    #     "errors": "JSON parse error - Expecting value: line 1 column 13 (char 12)",
    #     "status": 400,
    #     "title": "Invalid input json.",
    #     "type": "http://testserver/problems/error/",
    # }
    # expected_product_already_in_category: DetailError = {
    #     "detail": "Product is already in the category",
    #     "status": 400,
    #     "title": "A server error occurred.",
    #     "type": "http://testserver/problems/error/",
    # }
    #
    # expected_base_404: DetailError = {
    #     "detail": "Not Found",
    #     "status": 404,
    #     "title": "Resource not found",
    #     "type": "http://testserver/problems/not_found/",
    # }
    # expected_invalid_url_parameters: DetailError = {
    #     "detail": "Invalid parameters",
    #     "status": 400,
    #     "title": "Request has invalid parameters",
    #     "type": "http://testserver/problems/error/",
    # }
    # expected_duplicated_name_error: DetailError = {
    #     "detail": "This name already exists",
    #     "status": 400,
    #     "title": "A server error occurred.",
    #     "type": "http://testserver/problems/error/",
    # }
    # expected_invalid_status = {
    #     "detail": "Object was not Found",
    #     "errors": ["Status matching query does not exist."],
    #     "status": 404,
    #     "title": "Resource not found",
    #     "type": "http://testserver/problems/error/",
    # }
    # expected_nonexistent_product_error: DetailError = {
    #     "detail": "Product was not Found",
    #     "status": 400,
    #     "title": "Product not found",
    #     "type": "http://testserver/problems/error/",
    #     "errors": ["Product matching query does not exist."],
    # }
    # post_mock_product: ProductType = {
    #     "name": "Whopper",
    #     "price": 1.50,
    #     "description": "desc",
    # }
    #
    # invalid_mock_category_product: CategoryProductType = {"id": -1}
    #
    # invalid_json_data: str = '{"invalid": }'
    #
    # time_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"
    #
    # def setUp(self):
    #     self.test_product_1: Product = Product.objects.create(
    #         name="Burger", price=1.20, description="desc"
    #     )
    #     self.test_product_2: Product = Product.objects.create(
    #         name="Coke", price=1.50, description="desc"
    #     )
    #     self.test_product_3: Product = Product.objects.create(
    #         name="Chips", price=1.50, description="desc"
    #     )
    #
    #     self.test_cat_1: Category = Category.objects.create(
    #         name="Burgers", description="desc"
    #     )
    #     self.test_cat_2: Category = Category.objects.create(
    #         name="Sides", description="desc"
    #     )
    #
    #     self.test_cat_1.products.add(self.test_product_1)
    #     self.test_cat_1.products.add(self.test_product_2)
    #     self.test_cat_2.products.add(self.test_product_3)
    #
    #     self.test_order_empty: Order = Order.objects.create()
    #
    #     self.test_order_1: Order = Order.objects.create()
    #
    #     self.test_order_2: Order = Order.objects.create()
    #
    #     self.test_order_line_1 = LineItem.objects.create(
    #         order=self.test_order_1, product=self.test_product_1, quantity=2
    #     )
    #     self.test_order_line_2 = LineItem.objects.create(
    #         order=self.test_order_1, product=self.test_product_2, quantity=1
    #     )
    #     self.test_order_line_1.calculate_sub_total()
    #     self.test_order_line_2.calculate_sub_total()
    #     self.test_order_1.calculate_total()
    #
    # def assertJSONResponse(self, expected, actual, response, status_code):
    #     self.assertEqual(expected, actual)
    #     self.assertEqual(response.status_code, status_code)
    #
    # def assertJSONErrorResponse(self, expected, actual, response, status_code):
    #     self.assertIsInstance(actual.pop("traceId"), str)
    #     self.assertJSONResponse(expected, actual, response, status_code)
    #
    # def assertUpdateTime(self, expected, actual, response, status_code):
    #     actual_time: datetime = self.convert_time(actual["lastUpdated"])
    #     self.assertAlmostEqual(
    #         expected["lastUpdated"], actual_time, delta=timedelta(seconds=2)
    #     )
    #     self.assertIsInstance(actual.pop("lastUpdated"), str)
    #     self.assertIsInstance(expected.pop("lastUpdated"), datetime)
    #     self.assertJSONResponse(expected, actual, response, status_code)
    #
    # def assertCreateUpdateTime(self, expected, actual, response, status_code):
    #     actual_time: datetime = self.convert_time(actual["createdOn"])
    #     self.assertAlmostEqual(
    #         expected["createdOn"], actual_time, delta=timedelta(seconds=2)
    #     )
    #     self.assertIsInstance(actual.pop("createdOn"), str)
    #     self.assertIsInstance(expected.pop("createdOn"), datetime)
    #     self.assertUpdateTime(expected, actual, response, status_code)
    #
    # def convert_time(self, time_1):
    #     converted_time: datetime = datetime.strptime(time_1, self.time_format)
    #     return converted_time
    #
    # def get_mock_product_categories(
    #     self, product: Product
    # ) -> list[CategoryType]:
    #     return [
    #         {
    #             "id": category.id,
    #             "name": category.name,
    #             "description": category.description,
    #         }
    #         for category in Category.objects.filter(products=product)
    #     ]
    #
    # def get_mock_product_api(self, product: Product) -> ProductType:
    #     categories: list[CategoryType] = self.get_mock_product_categories(
    #         product
    #     )
    #     return {
    #         "id": product.id,
    #         "name": product.name,
    #         "price": product.price,
    #         "description": product.description,
    #         "categories": categories,
    #         "retired": product.retired,
    #     }
    #
    # def get_mock_category_product_api(
    #     self, product: Product
    # ) -> CategoryProductType:
    #     return {"id": product.id}
    #
    # def get_mock_category_api(
    #     self, category: Category, products: list[CategoryProductType]
    # ) -> CategoryType:
    #     return {
    #         "id": category.id,
    #         "name": category.name,
    #         "description": category.description,
    #         "createdOn": category.created_on.strftime(self.time_format),
    #         "lastUpdated": category.last_updated.strftime(self.time_format),
    #         "products": products,
    #         "retired": category.retired,
    #     }
    #
    # def get_category_and_product_for_order(
    #     self, product: Product
    # ) -> ProductType:
    #     categories: list[CategoryType] = self.get_mock_product_categories(
    #         product
    #     )
    #     return {
    #         "id": product.id,
    #         "name": product.name,
    #         "description": product.description,
    #         "price": float(product.price),
    #         "categories": categories,
    #     }
    #
    # def get_lineitem_for_order(self, order_line: LineItem) -> OrderProductType:
    #     return {
    #         "product": self.get_category_and_product_for_order(
    #             order_line.product
    #         ),
    #         "quantity": order_line.quantity,
    #         "subTotal": float(order_line.sub_total),
    #     }
    #
    # def get_mock_order_api(self, order: Order) -> OrderType:
    #     order_lines = [
    #         self.get_lineitem_for_order(order_line)
    #         for order_line in LineItem.objects.filter(order=order)
    #     ]
    #     return {
    #         "id": order.id,
    #         "createdOn": order.created_on.strftime(self.time_format),
    #         "lastUpdated": order.last_updated.strftime(self.time_format),
    #         "orderStatus": order.order_status,
    #         "orderTotal": float(order.order_total),
    #         "lineItems": order_lines,
    #     }
    #
    # def expected_order_after_put_request(
    #     self, order: Order, post_data: list
    # ) -> OrderType:
    #     old_order: OrderType = self.get_mock_order_api(order)
    #     expected_order: OrderType = old_order
    #     expected_order["lastUpdated"] = datetime.now()
    #     order_total: float = 0
    #     line_items: list = []
    #     for product_post_data in post_data:
    #         product: Product = Product.objects.get(
    #             id=product_post_data["product"]["id"]
    #         )
    #         quantity: int = product_post_data["quantity"]
    #         if product.retired or quantity < 1:
    #             continue
    #         sub_total: float = float(product.price * quantity)
    #         line_items.append(
    #             {
    #                 "product": self.get_category_and_product_for_order(
    #                     product
    #                 ),
    #                 "quantity": quantity,
    #                 "subTotal": sub_total,
    #             }
    #         )
    #         order_total += sub_total
    #
    #     expected_order["lineItems"] = line_items
    #     expected_order["orderTotal"] = float(order_total)
    #     return expected_order
    #
