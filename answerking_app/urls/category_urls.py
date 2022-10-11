from django.urls import path

from answerking_app.views import category_views

urlpatterns = [
    path("categories", category_views.CategoryListView.as_view(), name="category_list"),
    path(
        "categories/<cat_id>",
        category_views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "categories/<cat_id>/items/<item_id>",
        category_views.CategoryItemListView.as_view(),
        name="category_item_list",
    ),
]
