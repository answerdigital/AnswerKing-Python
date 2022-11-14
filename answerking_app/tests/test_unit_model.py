from decimal import Decimal

from django.test import TestCase

from answerking_app.models.models import Order, Item, Status


class ModelTests(TestCase):

    def setUp(self):
        self.status_pending: Status = Status.objects.create(status="Pending")

        self.test_item_1: Item = Item.objects.create(
            name="Burger",
            price=1.20,
            description="desc",
            stock=100,
            calories=100,
        )
        self.test_item_2: Item = Item.objects.create(
            name="Coke",
            price=1.50,
            description="desc",
            stock=100,
            calories=100,
        )
        self.test_item_3: Item = Item.objects.create(
            name="Chips",
            price=1.50,
            description="desc",
            stock=100,
            calories=100,
        )

        self.test_order_1: Order = Order.objects.create(
            address="123 Street, Leeds, LS73PP",
            status=self.status_pending,
            total=7.50,
        )

        self.test_order_1.order_items.add(
            self.test_item_1,
            through_defaults={"quantity": 1, "sub_total": self.test_item_1.price}
        )
        self.test_order_1.order_items.add(
            self.test_item_2,
            through_defaults={"quantity": 2, "sub_total": self.test_item_2.price*2}
        )
        self.test_order_1.order_items.add(
            self.test_item_3,
            through_defaults={"quantity": 1, "sub_total": self.test_item_3.price}
        )

    def tearDown(self):
        Item.objects.all().delete()
        Order.objects.all().delete()

    def test_models_calculate_total(self):
        init_tot: Decimal = self.test_order_1.total
        self.test_order_1.calculate_total()

        calculated_tot: Decimal = self.test_order_1.total
        expected_tot: Decimal = (self.test_item_1.price +
                                 (self.test_item_2.price * 2) +
                                 self.test_item_3.price
                                 )

        assert init_tot, 7.50
        assert calculated_tot, expected_tot
