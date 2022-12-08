from rest_framework.utils.serializer_helpers import ReturnDict

from answerking_app.models.serializers import ProductDetailSerializer
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class ProductDetailSerializerTests(UnitTestBase):

    utb = UnitTestBase()

    serializer_path: str = "answerking_app.models.serializers."
    test_product_serializer_data: dict[str | None] = utb.get_fixture(
        "products", "prod_id_only.json"
    )
    test_product_serializer: ProductDetailSerializer = ProductDetailSerializer(
        test_product_serializer_data
    )

    def test_product_detail_serializer_contains_correct_fields(self):
        data: ReturnDict = self.test_product_serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "id",
            ],
        )

    def test_product_detail_serializer_id_field_content(self):
        data: ReturnDict = self.test_product_serializer.data
        expected: int = self.test_product_serializer_data["id"]
        actual: int = data["id"]
        self.assertEqual(actual, expected)
