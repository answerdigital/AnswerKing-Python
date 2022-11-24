from decimal import Decimal

from django.test import TestCase

from answerking_app.models.models import Order, Product, LineItem
from answerking_app.tests.BaseTestClass import TestBase


class ModelTests(TestBase, TestCase):

    def test_calculate_total_with_line_items(self):
        test_order: Order = Order.objects.create()
        test_order_line_1 = LineItem.objects.create(order=test_order, product=self.test_product_1, quantity=2)
        test_order_line_2 = LineItem.objects.create(order=test_order, product=self.test_product_2, quantity=1)
        test_order_line_3 = LineItem.objects.create(order=test_order, product=self.test_product_3, quantity=2)
        test_order_line_1.calculate_sub_total()
        test_order_line_2.calculate_sub_total()
        test_order_line_3.calculate_sub_total()

        test_order.calculate_total()

        calculated_tot: Decimal = test_order.order_total
        expected_tot: Decimal = ((self.test_product_1.price * 2)
                                 + self.test_product_2.price
                                 + (self.test_product_3.price * 2)
                                 )

        self.assertEqual(calculated_tot, expected_tot)

    def test_calculate_total_without_line_items(self):
        test_order: Order = Order.objects.create()
        test_order.calculate_total()

        calculated_tot: Decimal = test_order.order_total
        expected_tot: Decimal = Decimal(0.00)

        self.assertEqual(calculated_tot, expected_tot)

    def test_calculate_total_without_sub_total_calculated(self):
        test_order: Order = Order.objects.create()
        test_order_line_1 = LineItem.objects.create(order=test_order, product=self.test_product_1, quantity=2)
        test_order.calculate_total()

        calculated_tot: Decimal = test_order.order_total
        expected_tot: Decimal = Decimal(0.00)

        self.assertEqual(calculated_tot, expected_tot)
        self.assertEqual(test_order_line_1.product.id, self.test_product_1.id)

    def test_calculate_sub_total(self):
        test_order: Order = Order.objects.create()
        test_order_line_1 = LineItem.objects.create(order=test_order, product=self.test_product_1, quantity=2)
        test_order_line_1.calculate_sub_total()

        calculated_sub_tot: Decimal = test_order_line_1.sub_total
        expected_sub_tot: Decimal = self.test_product_1.price * 2

        self.assertEqual(calculated_sub_tot, expected_sub_tot)
