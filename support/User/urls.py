from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view(), name='create_user'),
    path('token/obtain/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('token/verify/', TokenVerifyView.as_view(), name='verify_token'),
    path('update-data/<int:pk>/', views.UserDataAPIUpdate.as_view(), name='update-data'),
    path('change-password/<int:pk>/', views.UserChangePasswordAPIView.as_view(), name='change_password'), #!
    path('all-users/', views.AllUsersAPIView.as_view(), name='all_users'),
    path('only-support/', views.OnlySupportUsersAPIView.as_view(), name='only_support'),
    path('rights-support-contol/<int:pk>/', views.SupportControlAPIView.as_view(), name='support_contol')
]