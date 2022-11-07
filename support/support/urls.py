from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/v1/ticket/', include('Ticket.urls')),
    path('api/v1/user/', include('User.urls')),
]
