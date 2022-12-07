from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import UserCreateSerializer, LoginSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=self.request, user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
