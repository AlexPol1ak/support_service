from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsAdmin, IsAdminOrSupport, IsOwnerOrAdmin
from .serializers import (SupportsControlSerializer,
                          UserChangePasswordSerializer,
                          UserDataUpdateSerializer, UserSerializer)


class CreateUserAPIView(APIView):
    """View creates a new user."""

    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDataAPIUpdate(generics.RetrieveUpdateAPIView):
    """The view updates user data."""

    queryset = User
    serializer_class = UserDataUpdateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)


class UserChangePasswordAPIView(generics.UpdateAPIView):
    """The view changes the user's password."""
    queryset = User
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

class AllUsersAPIView(generics.ListAPIView):
    """The view displays all users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSupport,)


class OnlySupportUsersAPIView(generics.ListAPIView):
    """The view shows only the support staff."""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin, )

    def get_queryset(self):
        return User.objects.filter(is_support=True)


class SupportControlAPIView(generics.RetrieveUpdateAPIView):
    """The view issues and revokes the rights of the support worker."""

    queryset = User
    serializer_class = SupportsControlSerializer
    permission_classes = (IsAuthenticated, IsAdmin, )
