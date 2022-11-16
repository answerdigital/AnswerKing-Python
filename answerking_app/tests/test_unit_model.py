from decimal import Decimal

from django.test import TestCase

from answerking_app.models.models import Order, Item, Status
from answerking_app.tests.BaseTestClass import TestBase


class ModelTests(TestBase, TestCase):

    def test_calculate_total(self):
        """
        Test calculate total function. This function only
        depends on the sub_total values so set sub_total
        manually and set quantity to 0.
        """
        self.test_order_2.order_items.add(
            self.test_item_1,
            through_defaults={
                "quantity": 0,
                "sub_total": f"{self.test_item_1.price*1}"
            }
        )
        self.test_order_2.order_items.add(
            self.test_item_2,
            through_defaults={
                "quantity": 0,
                "sub_total": f"{self.test_item_2.price * 2}"
            }
        )
        self.test_order_2.order_items.add(
            self.test_item_3,
            through_defaults={
                "quantity": 0,
                "sub_total": f"{self.test_item_3.price * 1}"
            }
        )
        self.test_order_2.calculate_total()

        calculated_tot: Decimal = self.test_order_2.total
        accuracy = Decimal(10) ** -2
        expected_tot: Decimal = Decimal(
            self.test_item_1.price
            + (self.test_item_2.price * 2)
            + self.test_item_3.price
        ).quantize(accuracy)

        self.assertEqual(calculated_tot, expected_tot)
