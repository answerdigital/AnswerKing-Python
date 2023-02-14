from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from answerking_app.models.serializers import ManagerAuthSerializer


class RegisterCustomerView(
    generics.GenericAPIView,
):
    permission_classes = []
    serializer_class = []


class RegisterManagerView(
    generics.GenericAPIView,
):
    permission_classes = [IsAdminUser]
    serializer_class = ManagerAuthSerializer

