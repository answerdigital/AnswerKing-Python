from django.urls import path

from answerking_app.views import item_views

urlpatterns = [
    path("items", item_views.ItemListView.as_view(), name="item_list"),
    path("items/<item_id>", item_views.ItemDetailView.as_view(), name="item_detail"),
]
