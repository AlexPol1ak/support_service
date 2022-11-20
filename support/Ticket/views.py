from datetime import datetime

from django.http import HttpResponse
from django.utils import timezone
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
        request.data['user_id'] :int = self.request.user.pk
        serializer = serializers.CreateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class GetUsersTiketsAPIView(APIView):
    """Show all user tickets."""

    permission_classes = (IsAuthenticated, )

    # The user sees only his own tickets.
    def get(self, request):
        user_tickets  = Ticket.objects.filter(user_id=self.request.user.pk)
        user_data  = serializers.GetUsersTiketsSerializer(user_tickets, many=True).data
        return Response(user_data)


class CreateCommentAPIView(CreateAPIView):
    """Adds a comment to the ticket."""

    queryset = Comments.objects.all()
    serializer_class = serializers.CreateCommentSerializer
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
    """Shows support for all tickets"""

    queryset = Ticket.objects.all()
    serializer_class = serializers.GetAllTicketsSerializer
    permission_classes =(IsAuthenticated, user_permissions.IsAdminOrSupport, )


class ReplyTicketAPIView(APIView):
    """Allows support to reply to a ticket."""

    permission_classes = (IsAuthenticated, permissions.IsSupport)

    def put(self, request, *args, **kwargs):
        pk :int = kwargs.get('pk', None)
        if not pk:
            return Response({'Error': ' Specify ticket id'})

        try:
            ticket = Ticket.objects.get(pk=pk)
        except:
            return Response({'Error': 'Objects does not exists'})

        if ticket.resolved : #bool
            return Response({'result': f'Ticket {ticket.id} closed. Updating is not possible'})

        ticket.reply_date = timezone.now()
        ticket.support_id = request.user.pk

        if request.data.get('resolved', False):
            ticket.resolved_date = timezone.now()

        serializer = serializers.ReplyTicketSerializer(data=request.data, instance=ticket)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ReplyCommentAPIView(APIView):
    """Allow support to reply to a comment."""

    permission_classes = (IsAuthenticated, permissions.IsSupport)

    def put(self, request, *args, **kwargs):

        comment_id :int = kwargs.get('comment_id', None)

        if not comment_id:
            return Response({'error': 'The ID of comment is not specified.'})

        try:
            # comment = Comments.objects.filter(ticket_id=ticket_id, pk = comment_id)[0]
            # comment = Comments.objects.filter(ticket_id=ticket_id).get(pk=comment_id)
            comment = Comments.objects.get(pk=comment_id)
        except:
            return Response({'Error': f'Comment id{comment_id} does not exists'})

        if comment.ticket.resolved:
            return Response({'result': f'Ticket {comment.ticket_id} closed. Updating is not possible'})

        comment.support_id = request.user.pk
        comment.reply_date = timezone.now()

        serializer = serializers.ReplyCommentSerializer(data=request.data, instance=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        frozen :bool = serializer.data.get('frozen', None)
        resolved :bool = serializer.data.get('resolved', None)
        if frozen != None :
            comment.ticket.frozen = frozen
            comment.ticket.save()
        if resolved != None :
            comment.ticket.resolved_date = timezone.now()
            comment.ticket.resolved = resolved
            comment.ticket.save()

        return Response(serializer.data)

