from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, UserDataUpdateSerializer, UserChangePasswordSerializer, \
    SupportsControlSerializer


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDataAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = User
    serializer_class = UserDataUpdateSerializer
    # permission_classes = (IsAuthenticated,)


class UserChangePasswordAPIView(generics.UpdateAPIView):
    queryset = User
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

class AllUsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OnlySupportUsersAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_support=True)


class SupportControlAPIView(generics.RetrieveUpdateAPIView):
    queryset = User
    serializer_class = SupportsControlSerializer
