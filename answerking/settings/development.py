"""
Django development settings for answerking project.
"""
from answerking.settings.base import *

DEBUG = True

INSTALLED_APPS += (
    "coverage",
    "drf_yasg",
)

MIDDLEWARE.remove("django.middleware.csrf.CsrfViewMiddleware")

TEST_RUNNER = "snapshottest.django.TestRunner"