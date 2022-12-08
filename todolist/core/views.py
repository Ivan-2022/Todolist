from django.contrib.auth import login, logout
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import User
from .serializers import UserCreateSerializer, LoginSerializer, ProfileSerializer


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


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
