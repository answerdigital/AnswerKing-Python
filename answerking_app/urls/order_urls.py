from functools import partial

from django.urls import path

from answerking_app.views import order_views

urlpatterns: list[partial] = [
    path("orders", order_views.OrderListView.as_view(), name="order_list"),
    path(
        "orders/<int:order_id>",
        order_views.OrderDetailView.as_view(),
        name="order_detail",
    ),
    path(
        "orders/<int:order_id>/orderline/<int:product_id>",
        order_views.OrderProductListView.as_view(),
        name="order_product_list",
    ),
]
