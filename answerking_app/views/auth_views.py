from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from answerking_app.models.permissions.auth_permissions import IsManagerUser
from answerking_app.models.serializers import ManagerAuthSerializer, \
    LoginSerializer


class RegisterManagerView(
    generics.CreateAPIView,
):
    permission_classes = (AllowAny,)
    serializer_class = ManagerAuthSerializer


class LoginView(
    TokenObtainPairView,
):
    serializer_class = LoginSerializer
