from functools import partial

from django.urls import path

from answerking_app.views import category_views

urlpatterns: list[partial] = [
    path(
        "categories",
        category_views.CategoryListView.as_view(),
        name="category_list",
    ),
    path(
        "categories/<pk>",
        category_views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "categories/<cat_id>/products",
        category_views.CategoryProductListView.as_view(),
        name="category_product_list",
    ),
]
