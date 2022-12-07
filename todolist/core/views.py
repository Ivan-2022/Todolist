from rest_framework import generics

from .serializers import UserCreateSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
