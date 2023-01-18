
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]