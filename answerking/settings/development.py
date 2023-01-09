"""
Django development settings for answerking project.
"""
import answerking.settings.base as akb

DEBUG = True

akb.INSTALLED_APPS += (
    "coverage",
    "drf_yasg",
)

akb.MIDDLEWARE.remove("django.middleware.csrf.CsrfViewMiddleware")

TEST_RUNNER = "snapshottest.django.TestRunner"
