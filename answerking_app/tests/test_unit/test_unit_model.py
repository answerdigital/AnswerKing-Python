from decimal import Decimal

from answerking_app.models.models import Order, Product, LineItem
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class ModelTests(UnitTestBase):
    UTB = UnitTestBase()

    def test_calculate_total_with_line_items(self):
        to_seed = {
            "margarita_pizza_data.json": "products",
            "pepperoni_pizza_data.json": "products",
        }
        self.seed_data(to_seed)
        prod_1 = Product.objects.get(name="Margarita pizza")
        quant_1 = 2
        quant_2 = 1
        prod_2 = Product.objects.get(name="Pepperoni pizza")
        test_order: Order = Order.objects.create()
        test_order_line_1 = LineItem.objects.create(
            order=test_order, product=prod_1, quantity=quant_1
        )
        test_order_line_2 = LineItem.objects.create(
            order=test_order, product=prod_2, quantity=quant_2
        )
        test_order_line_1.calculate_sub_total()
        test_order_line_2.calculate_sub_total()

        test_order.calculate_total()

        calculated_tot: Decimal = test_order.order_total
        expected_tot: Decimal = Decimal(
            (prod_1.price * quant_1) + (prod_2.price * quant_2)
        ).quantize(Decimal("0.00"))

        self.assertEqual(calculated_tot, expected_tot)

    def test_calculate_total_without_line_items(self):
        test_order: Order = Order.objects.create()
        test_order.calculate_total()

        calculated_tot: Decimal = test_order.order_total
        expected_tot: Decimal = Decimal(0.00)

        self.assertEqual(calculated_tot, expected_tot)

    def test_calculate_total_without_sub_total_calculated(self):
        to_seed = {"margarita_pizza_data.json": "products"}
        self.seed_data(to_seed)
        prod = Product.objects.get(name="Margarita pizza")
        quant = 1
        test_order: Order = Order.objects.create()
        test_order_line_1 = LineItem.objects.create(
            order=test_order, product=prod, quantity=quant
        )
        test_order.calculate_total()

        calculated_tot: Decimal = test_order.order_total
        expected_tot: Decimal = Decimal(0.00)

        self.assertEqual(calculated_tot, expected_tot)
        self.assertEqual(test_order_line_1.product.id, prod.id)
        self.assertEqual(test_order_line_1.quantity, quant)

    def test_calculate_sub_total(self):
        to_seed = {"margarita_pizza_data.json": "products"}
        self.seed_data(to_seed)
        prod = Product.objects.get(name="Margarita pizza")
        quant = 2
        test_order: Order = Order.objects.create()
        test_order_line_1 = LineItem.objects.create(
            order=test_order, product=prod, quantity=quant
        )
        test_order_line_1.calculate_sub_total()
        calculated_sub_tot: Decimal = test_order_line_1.sub_total
        expected_sub_tot: Decimal = prod.price * 2

        self.assertEqual(calculated_sub_tot, expected_sub_tot)
        self.assertEqual(test_order_line_1.product.id, prod.id)
        self.assertEqual(test_order_line_1.quantity, quant)
