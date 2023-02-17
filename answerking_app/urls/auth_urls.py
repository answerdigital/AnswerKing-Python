from functools import partial

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from answerking_app.views import auth_views

urlpatterns: list[partial] = [
    path(
        "register/manager",
        auth_views.RegisterManagerView.as_view(),
        name="register_manager",
    ),
    path("login", auth_views.LoginView.as_view(), name="token_obtain_pair"),
    path("login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout", TokenBlacklistView.as_view(), name="token_blacklist"),
]
