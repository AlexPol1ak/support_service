from django.http import JsonResponse
from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsAdmin, IsAdminOrSupport, IsOwnerOrAdmin
from .serializers import (SupportsControlSerializer,
                          UserChangePasswordSerializer,
                          UserDataUpdateSerializer, UserSerializer)


def test_page(request):
    return JsonResponse({'Home page': "start test pages"})

class CreateUserAPIView(APIView):
    """Представление для регистрации нового пользователя."""

    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDataAPIUpdate(generics.RetrieveUpdateAPIView):
    """Представление для получения или обновления данных пользователем."""

    queryset = User
    serializer_class = UserDataUpdateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)


class UserChangePasswordAPIView(generics.UpdateAPIView):
    """Предсталвение для изменения пользователем пароля."""
    queryset = User
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

class AllUsersAPIView(generics.ListAPIView):
    """Представление для отображения всех пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSupport,)


class OnlySupportUsersAPIView(generics.ListAPIView):
    """Предсталвение для отображения только агентов поддержки."""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin, )

    def get_queryset(self):
        return User.objects.filter(is_support=True)


class SupportControlAPIView(generics.RetrieveUpdateAPIView):
    """Предсталвение для назначения или разжалования агентов поддержки."""

    queryset = User
    serializer_class = SupportsControlSerializer
    permission_classes = (IsAuthenticated, IsAdmin, )
