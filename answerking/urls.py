from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path("api/", include("answerking_app.urls.product_urls")),
    path("api/", include("answerking_app.urls.category_urls")),
    path("api/", include("answerking_app.urls.order_urls")),
    path("admin/", admin.site.urls),
    path("", include("drf_problems.urls")),
]

if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]
