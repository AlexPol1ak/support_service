
from django.contrib import admin
from django.urls import path, include, re_path

from Ticket.views import error404

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/v1/ticket/', include('Ticket.urls')),
    path('api/v1/user/', include('User.urls')),
    re_path(r'^.*/$', error404, name='error404'),
]



