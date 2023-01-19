from functools import partial

from django.urls import path

from answerking_app.views import order_views

urlpatterns: list[partial] = [
    path("orders", order_views.OrderListView.as_view(), name="order_list"),
    path(
        "orders/<pk>",
        order_views.OrderDetailView.as_view(),
        name="order_detail",
    ),
]
