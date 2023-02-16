from functools import partial

from django.urls import path

from answerking_app.views import product_views

urlpatterns: list[partial] = [
    path(
        "products",
        product_views.ProductView.as_view(),
        name="product_list",
    ),
    path(
        "products/<pk>",
        product_views.ProductIdView.as_view(),
        name="product_detail",
    ),
]
