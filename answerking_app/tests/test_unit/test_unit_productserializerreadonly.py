from decimal import Decimal

from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.serializers import ProductSerializerReadOnly
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class ProductSerializerTests(UnitTestBase):

    utb = UnitTestBase()

    serializer_path: str = "answerking_app.models.serializers."
    test_product_serializer_data: dict[str | None] = utb.get_fixture(
        "products", "product_lineitem_data.json"
    )
    test_product_serializer: ProductSerializerReadOnly = ProductSerializerReadOnly(
        test_product_serializer_data
    )

    def test_product_serializer_contains_correct_fields(self):
        data: ReturnDict = self.test_product_serializer.instance
        self.assertCountEqual(
            data.keys(),
            [
                "id",
                "name",
                "description",
                "price",
                "categories",
            ]
        )
