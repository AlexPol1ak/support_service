from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.ticket_test, name='ticket_test'),
    path('create-ticket/', views.CreateTicketAPIView.as_view(), name='create_ticket'),
    path('my-tickets/', views.GetUsersTiketsAPIView.as_view(), name='get_users_tickets'),
    path('ticket/<int:pk>/', views.DetailTicketAPIView.as_view(), name='detail_ticket')
]