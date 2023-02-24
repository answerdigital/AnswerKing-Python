from functools import partial

from django.urls import path

from answerking_app.views import category_views

urlpatterns: list[partial] = [
    path(
        "categories",
        category_views.CategoryView.as_view(),
        name="category",
    ),
    path(
        "categories/<pk>",
        category_views.CategoryIdView.as_view(),
        name="category_id",
    ),
    path(
        "categories/<pk>/products",
        category_views.CategoryProductView.as_view(),
        name="category_product",
    ),
]
