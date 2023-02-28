"""
Django development settings for answerking project.
"""
from answerking.settings.base import *

DEBUG = True

INSTALLED_APPS += (
    "coverage",
    "drf_spectacular",
)
ALLOWED_HOSTS = ["*"]


MIDDLEWARE.remove("django.middleware.csrf.CsrfViewMiddleware")

TEST_RUNNER = "snapshottest.django.TestRunner"

REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"

SPECTACULAR_SETTINGS = {
    "TITLE": "Answerking Python API",
    "DESCRIPTION": "Django API schema for Answerking Python project",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
