from functools import partial

from django.urls import path

from answerking_app.views import tag_views

urlpatterns: list[partial] = [
    path(
        "tags",
        tag_views.TagListView.as_view(),
        name="tag_list",
    ),
    path(
        "tags/<pk>",
        tag_views.TagDetailView.as_view(),
        name="product_detail",
    ),
]
