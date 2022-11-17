from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.ticket_test, name='ticket_test'),
    path('create-ticket/', views.CreateTicketAPIView.as_view(), name='create_ticket'),
    path('my-tickets/', views.GetUsersTiketsAPIView.as_view(), name='get_users_tickets'),
    path('ticket/<int:pk>/', views.DetailTicketAPIView.as_view(), name='detail_ticket'),
    path('add-comment/', views.CreateCommentAPIView.as_view(), name='add_comment'),
    path('get-all-tickets/', views.GetAllTicketsAPIView.as_view(), name='get_all_tickets'),
    path('reply-ticket/<int:pk>/', views.ReplyTicketAPIView.as_view(), name='reply_ticket'),
]