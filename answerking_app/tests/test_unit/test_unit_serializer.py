from answerking_app.models.serializers import (
    compress_white_spaces,
)
from answerking_app.tests.test_unit.UnitTestBaseClass import UnitTestBase


class SerializerTests(UnitTestBase):
    def test_compress_white_spaces_fn(self):
        test_str: str = "  White   Spaces    "
        expected: str = "White Spaces"
        actual: str = compress_white_spaces(test_str)

        self.assertEqual(expected, actual)
