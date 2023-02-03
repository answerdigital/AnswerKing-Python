from django.test import Client
from assertpy import assert_that
from ddt import ddt, data

from answerking_app.tests.test_integration.IntegrationTestBaseClass import (
    IntegrationTestBase,
)

client = Client()


@ddt()
class GetTests(IntegrationTestBase):
    def test_get_all_returns_no_content(self):
        response = client.get("/api/tags")
        assert_that(response.json()).is_equal_to([])
        assert_that(response.status_code).is_equal_to(200)


class PostTests(IntegrationTestBase):
    pass


class PutTests(IntegrationTestBase):
    pass


class DeleteTests(IntegrationTestBase):
    pass

