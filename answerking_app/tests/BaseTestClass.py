from datetime import datetime, timedelta
import json

from answerking_app.models.models import Category, Product, Order, LineItem
from answerking_app.utils.model_types import (
    CategoryType,
    DetailError,
    ProductType,
    OrderType,
    OrderProductType,
    CategoryProductType,
)


class TestBase:
    def setUp(self):
        Item.objects.all().delete()
        Category.objects.all().delete()
        Status.objects.all().delete()
        Order.objects.all().delete()

    def seedFixture(self, type, fixtureName):
        if type == "items":
            data = self.getFixture(type, fixtureName)
            if isinstance(data, list):
                for item in data:
                    Item.objects.create(**item)
            elif isinstance(data, dict):
                Item.objects.create(**data)
            else:
                raise Exception(f"{data} is not valid json")
            return data
        else:
            raise Exception(f"{type} is not a valid data seeding type")

    def getFixture(self, type, fixtureName):
        fixturePath = "answerking_app/tests/fixtures"
        return json.load(open(f"{fixturePath}/{type}/{fixtureName}"))

        # Item.objects.create(**data)

        # self.test_item_1: Item = Item.objects.create(
        #     id="1",
        #     name="Burger",
        #     price=1.20,
        #     description="desc",
        #     stock=100,
        #     calories=100,
        # )
        # self.test_item_2: Item = Item.objects.create(
        #     id="2",
        #     name="Coke",
        #     price=1.50,
        #     description="desc",
        #     stock=100,
        #     calories=100,
        # )
        # self.test_item_3: Item = Item.objects.create(
        #     id="3",
        #     name="Chips",
        #     price=1.50,
        #     description="desc",
        #     stock=100,
        #     calories=100,
        # )

        # self.test_cat_1: Category = Category.objects.create(name="Burgers")
        # self.test_cat_2: Category = Category.objects.create(name="Sides")

        # self.test_cat_1.items.add(self.test_item_1)
        # self.test_cat_1.items.add(self.test_item_2)
        # self.status_pending: Status = Status.objects.create(status="Pending")
        # self.status_complete: Status = Status.objects.create(
        #     status="Completed"
        # )

        # self.test_order_empty: Order = Order.objects.create(
        #     address="123A3 Street, Leeds, LS17PP",
        #     status=self.status_pending,
        # )

        # self.test_cat_1.products.add(self.test_product_1)
        #self.test_cat_1.products.add(self.test_product_2)
        # self.test_cat_2.products.add(self.test_product_3)

        # self.test_order_empty: Order = Order.objects.create()

        # self.test_order_1: Order = Order.objects.create()

        # self.test_order_2: Order = Order.objects.create(
        #     address="456 Test Lane, Bradford, BD30PA",
        #     status=self.status_pending,
        # )

        # self.test_order_1.order_items.add(
        #     self.test_item_1,
        #     through_defaults={
        #         "quantity": 2,
        #         "sub_total": f"{self.test_item_1.price * 2:.2f}",
        #     },
        # )

        # self.test_order_1.order_items.add(
        #     self.test_item_2,
        #     through_defaults={
        #         "quantity": 1,
        #         "sub_total": f"{self.test_item_2.price:.2f}",
        #     },
        # )
        # self.test_order_1.calculate_total()

    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        Order.objects.all().delete()

    def assertJSONErrorResponse(self, response):
        self.assertIsInstance(response.pop("traceId"), str)  # type: ignore[reportGeneralTypeIssues]
        self.assertMatchSnapshot(response)

    def get_mock_category_api(
        self, category: Category, products: list[CategoryProductType]
    ) -> CategoryType:
        return {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "createdOn": category.created_on.strftime(self.time_format),
            "lastUpdated": category.last_updated.strftime(self.time_format),
            "products": products,
            "retired": category.retired,
        }

    def get_category_and_product_for_order(
        self, product: Product
    ) -> ProductType:
        categories: list[CategoryType] = self.get_mock_product_categories(
            product
        )
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "categories": categories,
        }

    def get_lineitem_for_order(self, order_line: LineItem) -> OrderProductType:
        return {
            "product": self.get_category_and_product_for_order(
                order_line.product
            ),
            "quantity": order_line.quantity,
            "subTotal": float(order_line.sub_total),
        }

    def get_mock_order_api(self, order: Order) -> OrderType:
        order_lines = [
            self.get_lineitem_for_order(order_line)
            for order_line in LineItem.objects.filter(order=order)
        ]
        return {
            "id": order.id,
            "createdOn": order.created_on.strftime(self.time_format),
            "lastUpdated": order.last_updated.strftime(self.time_format),
            "orderStatus": order.order_status,
            "orderTotal": float(order.order_total),
            "lineItems": order_lines,
        }

    def expected_order_after_put_request(
        self, order: Order, post_data: list
    ) -> OrderType:
        old_order: OrderType = self.get_mock_order_api(order)
        expected_order: OrderType = old_order
        expected_order["lastUpdated"] = datetime.now()
        order_total: float = 0
        line_items: list = []
        for product_post_data in post_data:
            product: Product = Product.objects.get(
                id=product_post_data["product"]["id"]
            )
            quantity: int = product_post_data["quantity"]
            if product.retired or quantity < 1:
                continue
            sub_total: float = float(product.price * quantity)
            line_items.append(
                {
                    "product": self.get_category_and_product_for_order(
                        product
                    ),
                    "quantity": quantity,
                    "subTotal": sub_total,
                }
            )
            order_total += sub_total

        expected_order["lineItems"] = line_items
        expected_order["orderTotal"] = float(order_total)
        return expected_order
