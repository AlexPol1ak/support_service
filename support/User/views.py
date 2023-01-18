from django.http import JsonResponse
from drf_spectacular.utils import extend_schema

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
    """Регистрация нового пользователя."""

    permission_classes = (AllowAny,)

    @extend_schema(request=UserSerializer, responses=UserSerializer,)
    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDataAPIUpdate(generics.RetrieveUpdateAPIView):
    """
    Получение или обновление данных пользователем.
    При использовании методов put, patch, не одно передаваймое значение в body не является обязательным.
    """

    queryset = User
    serializer_class = UserDataUpdateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)


class UserChangePasswordAPIView(generics.UpdateAPIView):
    """Изменение пользователем пароля."""

    queryset = User
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

class AllUsersAPIView(generics.ListAPIView):
    """Отображает всех пользователей. Доступно только для администратора и агентов поддержки"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSupport,)


class OnlySupportUsersAPIView(generics.ListAPIView):
    """Отображает только агентов поддержки. Доступно только для администратора"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin, )

    def get_queryset(self):
        return User.objects.filter(is_support=True)


class SupportControlAPIView(generics.RetrieveUpdateAPIView):
    """Назначение или разжалование агентов поддержки. Доступно только для администратора"""

    queryset = User
    serializer_class = SupportsControlSerializer
    permission_classes = (IsAuthenticated, IsAdmin, )
