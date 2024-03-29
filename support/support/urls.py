
from django.contrib import admin
from django.urls import include, path, re_path

from Ticket.views import error404
from User.views import test_page

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', test_page),
    path('api/v1/user/', include('User.urls')),
    path('api/v1/ticket/', include('Ticket.urls')),
    path('api/doc/', include('APIDoc.urls')),
    re_path(r'^.*/$', error404, name='error404'),
]



