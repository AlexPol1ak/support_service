from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from kombu.exceptions import OperationalError
from rest_framework import viewsets
from rest_framework.exceptions import NotFound

import User.permissions as user_permissions
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Ticket import permissions, serializers
from Ticket.models import Comments, Ticket
from Ticket.service import send_reply_user
from Ticket.tasks import send_email_user_celery, send_reply_comment_user_celery
from User.models import User


def error404(request):
    return JsonResponse({'code': '404','detail': 'Page not found'}, status=404)



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
        """The request creates a new ticket."""

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
        """The request returns to the user all his tickets."""

        user_tickets = Ticket.objects.filter(user_id=self.request.user.pk)
        user_data = serializers.GetUsersTiketsSerializer(user_tickets, many=True).data
        return Response(user_data)

class DetailTicketAPIView(APIView):
    """Displays details of the ticket."""
    # The author of the ticket and support can get detailed information about the ticket.
    permission_classes = (IsAuthenticated, permissions.IsAuthorsObjectOrSupport)
    raise_exception = True

    def get(self, request, pk):
        """The request returns all information about the ticket with comments."""

        try:
            ticket = Ticket.objects.get(pk=pk)
        except:
            return Response ({'ticket': 'Ticket not found'})

        ticket_data = serializers.DetailTicketSerializer(ticket).data
        self.check_object_permissions(self.request, ticket)

        return Response(ticket_data)


#alternative
class GetUsersTicketViewSet(viewsets.ReadOnlyModelViewSet):
    """Returns to the user a list of his requests or one selected request in detail."""
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Returns all objects of the author or one object in detail."""
        if self.action == 'list':
            return Ticket.objects.filter(user_id=self.request.user.pk)
        elif self.action == 'retrieve':
            return Ticket.objects.filter(pk=self.kwargs.get('pk'))
    def get_serializer_class(self):
        """Returns a serializer for all tickets of one author or a serializer for one detailed ticket."""

        if self.action == "list":
            return serializers.GetUsersTiketsSerializer
        elif self.action == 'retrieve':
            return serializers.DetailTicketSerializer
        else:
            raise AttributeError("Specify the action. For example .as_view('get': 'list')")


class CreateCommentAPIView(CreateAPIView):
    """Adds a comment to the ticket."""

    queryset = Comments.objects.all()
    serializer_class = serializers.CreateCommentSerializer
    # Add a comment to the ticket can the author of the ticket,
    # and if the ticket is not frozen and not closed by support.
    permission_classes = (IsAuthenticated, permissions.IsOwner ,permissions.TicketNotFrozenAndClosed)




class GetAllTicketsAPIView(ListAPIView):
    """Shows support for all tickets"""

    queryset = Ticket.objects.all()
    serializer_class = serializers.GetAllTicketsSerializer
    permission_classes =(IsAuthenticated, user_permissions.IsAdminOrSupport, )


class ReplyTicketAPIView(APIView):
    """Allows support to reply to a ticket."""

    permission_classes = (IsAuthenticated, permissions.IsSupport)

    def put(self, request, *args, **kwargs):
        """The request saves the support response to the ticket. Sends notification of the response to the user."""

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
        resolved = request.data.get('resolved', None)
        frozen = request.data.get('frozen', None)

        if resolved:
            ticket.resolved_date = timezone.now()

        serializer = serializers.ReplyTicketSerializer(data=request.data, instance=ticket)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            send_email_user_celery.apply_async((
                User.objects.get(pk=ticket.user_id).email,
                ticket.title,
                request.user.first_name, # <-support_name
                ticket.support_response,
                frozen,
                resolved
                ), queue='ticket')
        except OperationalError:
            pass
            # print("Send reply ticket in email error")

        return Response(serializer.data)



class ReplyCommentAPIView(APIView):
    """Allow support to reply to a comment."""

    permission_classes = (IsAuthenticated, permissions.IsSupport)

    def put(self, request, *args, **kwargs):
        """The request saves the support response to the comment.
        Sends a notification to the user's email in the background.
        """

        comment_id :int = kwargs.get('comment_id', None)
        if not comment_id:
            return Response({'error': 'The ID of comment is not specified.'})

        try:
            # comment = Comments.objects.filter(ticket_id=ticket_id, pk = comment_id)[0]
            # comment = Comments.objects.filter(ticket_id=ticket_id).get(pk=comment_id)
            comment = Comments.objects.get(id=comment_id)
        except:
            return Response({'Error': f'Comment id {comment_id} does not exists'})


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
        try:
            send_reply_comment_user_celery.apply_async((
                User.objects.get(pk=comment.ticket.user_id).email,
                comment.ticket.title,
                request.user.first_name,
                comment.user_comment,
                request.data.get('support_response',''),
                frozen,
                resolved
            ), queue='comments')
        except OperationalError:
            pass
            # print('send reply comment in email error')

        return Response(serializer.data)

