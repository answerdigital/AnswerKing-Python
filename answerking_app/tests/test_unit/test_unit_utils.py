from answerking_app.models.models import Product
from answerking_app.utils.url_parameter_check import check_url_parameter

from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class UtilsTests(UnitTestBase):

    utb = UnitTestBase()

    test_prod_data: dict = utb.get_fixture(
        "products", "plain_burger_data.json"
    )

    def setUp(self):
        prod: Product = Product.objects.create(**self.test_prod_data)

    def tearDown(self):
        Product.objects.all().delete()

    def test_check_url_parameter_valid_pk(self):
        test_prod: Product = Product.objects.get(
            name=self.test_prod_data["name"]
        )
