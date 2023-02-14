from functools import partial

from django.urls import path

from answerking_app.views import auth_views

urlpatterns: list[partial] = [
    path(
        "register/manager",
        auth_views.RegisterManagerView.as_view(),
        name="register_manager"
    ),
]
