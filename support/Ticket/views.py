from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Ticket.models import Ticket, Comments
from Ticket import permissions
from Ticket import serializers
import User.permissions as user_permissions

def ticket_test(request):
    return HttpResponse("Ticket test page")


# Alternative option
# class CreateTicketAPIView(CreateAPIView):
#     """Creates a new ticket."""
#     queryset = Ticket.objects.all()
#     serializer_class = CreateTicketSerializer
#     # permission_classes = (IsAuthenticated,)


class CreateTicketAPIView(APIView):
    """Creates a new ticket."""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data['user_id'] = self.request.user.pk
        serializer = serializers.CreateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class GetUsersTiketsAPIView(APIView):
    """Show all user tickets."""

    permission_classes = (IsAuthenticated, )

    # The user sees only his own tickets.
    def get(self, request):
        user_tickets = Ticket.objects.filter(user_id=self.request.user.pk)
        user_data = serializers.GetUsersTiketsSerializer(user_tickets, many=True).data
        return Response(user_data)


class CreateCommentAPIView(CreateAPIView):
    """Adds a comment to the ticket."""

    queryset = Comments.objects.all()
    serializer_class = serializers.CreateCommnetSerilizer
    # Add a comment to the ticket can the author of the ticket,
    # and if the ticket is not frozen and not closed by support.
    permission_classes = (IsAuthenticated, permissions.IsOwner ,permissions.TicketNotFrozenAndClosed)


class DetailTicketAPIView(APIView):
    """Displays details of the ticket."""
    # The author of the ticket and support can get detailed information about the ticket.
    permission_classes = (IsAuthenticated, permissions.IsAuthorsObjectOrSupport)

    def get(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except:
            return Response ({'ticket': 'Ticket not found'})
        ticket_data = serializers.DetailTicketSerializer(ticket).data
        self.check_object_permissions(self.request, ticket)
        return Response(ticket_data)


class GetAllTicketsAPIView(ListAPIView):

    queryset = Ticket.objects.all()
    serializer_class = serializers.GetAllTicketsSerilizers
    permission_classes =(IsAuthenticated, user_permissions.IsAdminOrSupport, )
