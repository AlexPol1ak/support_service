from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Ticket.models import Ticket
from Ticket import permissions
from Ticket import serializers



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
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_tickets = Ticket.objects.filter(user_id=self.request.user.pk)
        user_data = serializers.GetUsersTiketsSerializer(user_tickets, many=True).data
        return Response(user_data)


class DetailTicketAPIView(APIView):

    permission_classes = (IsAuthenticated, permissions.IsAuthorsObjectOrSupport)

    def get(self, request, pk):

        ticket = Ticket.objects.get(pk=pk)
        ticket_data = serializers.DetailTicketSerializer(ticket).data
        self.check_object_permissions(self.request, ticket)
        return Response(ticket_data)
