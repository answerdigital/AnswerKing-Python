from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path("api/", include("answerking_app.urls.item_urls")),
    path("api/", include("answerking_app.urls.category_urls")),
    path("api/", include("answerking_app.urls.order_urls")),
    path("admin/", admin.site.urls),
    path("", include("drf_problems.urls")),
]

if settings.DEBUG:
    from django.urls import re_path
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions

    schema_view = get_schema_view(
        openapi.Info(
            title="AnswerKing Python API",
            default_version="v1",
            description="Test description",
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )
    urlpatterns += [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            r"api/swagger",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]
