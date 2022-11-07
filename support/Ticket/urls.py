from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.ticket_test, name='ticket_test')
]