
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from drf_spectacular.utils import extend_schema, inline_serializer

from kombu.exceptions import OperationalError
from rest_framework import viewsets
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import User.permissions as user_permissions
from Ticket import permissions, serializers
from Ticket.models import Comments, Ticket
from Ticket.service import send_reply_user
from Ticket.tasks import send_email_user_celery, send_reply_comment_user_celery
from User.models import User


def error404(request):
    """Представление для исключения 404 страница не найдена."""
    return JsonResponse({'code': '404','detail': 'Page not found'}, status=404)



# Alternative option
# class CreateTicketAPIView(CreateAPIView):
#     """Creates a new ticket."""
#     queryset = Ticket.objects.all()
#     serializer_class = CreateTicketSerializer
#     # permission_classes = (IsAuthenticated,)


class CreateTicketAPIView(APIView):
    """Создает новое обращение пользователя."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(request=inline_serializer(
                       name='InlineCreateTicketSerializer',
                       fields={'title': serializers.serializers.CharField(),
                               'user_message': serializers.serializers.CharField()
                               }
                   ),
                   responses=serializers.CreateTicketSerializer)
    def post(self, request):
        """Запрос создает новое обращение пользователя."""

        request.data['user_id'] :int = self.request.user.pk
        serializer = serializers.CreateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class GetUsersTiketsAPIView(APIView):
    """Возвращает пользователю все его обращения."""

    permission_classes = (IsAuthenticated, )

    # The user sees only his own tickets.
    @extend_schema(responses=serializers.GetUsersTiketsSerializer(many=True),
                   request=serializers.GetUsersTiketsSerializer)
    def get(self, request):
        """Запрос возвращает пользователю все его обращения."""

        user_tickets = Ticket.objects.filter(user_id=self.request.user.pk)
        user_data = serializers.GetUsersTiketsSerializer(user_tickets, many=True).data
        return Response(user_data)


class DetailTicketAPIView(APIView):
    """Возвращает пользователю детальное отображение обращения."""
    # The author of the ticket and support can get detailed information about the ticket.
    permission_classes = (IsAuthenticated, permissions.IsAuthorsObjectOrSupport)
    raise_exception = True
    @extend_schema(responses=serializers.DetailTicketSerializer)
    def get(self, request, pk):
        """Запрос возвращает пользователю детальное отображение обращения."""

        try:
            ticket = Ticket.objects.get(pk=pk)
        except:
            return Response ({'ticket': 'Ticket not found'})

        ticket_data = serializers.DetailTicketSerializer(ticket).data
        self.check_object_permissions(self.request, ticket)

        return Response(ticket_data)


#alternative
class GetUsersTicketViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращает пользователю список его запросов или один выбранный запрос в детально."""
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Возвращает все обращения автора или одно обращение детально."""
        if self.action == 'list':
            return Ticket.objects.filter(user_id=self.request.user.pk)
        elif self.action == 'retrieve':
            return Ticket.objects.filter(pk=self.kwargs.get('pk'))
    def get_serializer_class(self):
        """Возвращает сериализатор для всех обращений одного автора или сериализатор для одного детального обращения."""

        if self.action == "list":
            return serializers.GetUsersTiketsSerializer
        elif self.action == 'retrieve':
            return serializers.DetailTicketSerializer
        else:
            raise AttributeError("Specify the action. For example .as_view('get': 'list')")


class CreateCommentAPIView(CreateAPIView):
    """
    Добавляет комментарий к обращению от пользователя.
    Добавить комментарий к обращению может автор обращения,
    и если обращение не заморожено и не закрыто службой поддержки.
    """

    queryset = Comments.objects.all()
    serializer_class = serializers.CreateCommentSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwner ,permissions.TicketNotFrozenAndClosed)


class GetAllTicketsAPIView(ListAPIView):
    """Отображает агентам поддержки все обращения."""

    queryset = Ticket.objects.all()
    serializer_class = serializers.GetAllTicketsSerializer
    permission_classes =(IsAuthenticated, user_permissions.IsAdminOrSupport, )


class ReplyTicketAPIView(APIView):
    """Создает ответ на обращение агента поддержки."""

    permission_classes = (IsAuthenticated, permissions.IsSupport)

    @extend_schema(request=inline_serializer(
                       name='InlineReplyTicketSerializer',
                       fields={'support_response': serializers.serializers.CharField(),
                               'frozen': serializers.serializers.BooleanField(),
                               'resolved': serializers.serializers.BooleanField(),
                               },
                   ),
                   responses=serializers.ReplyTicketSerializer)
    def put(self, request, *args, **kwargs):
        """
        Запрос сохраняет ответ агента поддержки на обращение. Отправляет уведомление пользователю на email.
        Все передаваймые значения не обязательны.
        """

        pk :int = kwargs.get('pk', None)
        if not pk:
            return Response({'Error': ' Specify ticket id'})

        try:
            ticket = Ticket.objects.get(pk=pk)
        except:
            return Response({'Error': 'Objects does not exists'})


        if ticket.resolved : #bool
            return Response({'result': f'Ticket {ticket.id} closed. Updating is not possible'})

        request.data['support_id'] = request.user.pk
        ticket.reply_date = timezone.now()
        resolved = request.data.get('resolved', None)
        frozen = request.data.get('frozen', None)
        ticket.save()

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
            print("Send reply ticket in email error")

        return Response(serializer.data)



class ReplyCommentAPIView(APIView):
    """Создает ответ на комментарий пользователя к своему обращению. Отправляет уведомление на email."""

    permission_classes = (IsAuthenticated, permissions.IsSupport)
    @extend_schema(request=serializers.ReplyCommentSerializer, responses=serializers.ReplyCommentSerializer)
    def put(self, request, *args, **kwargs):
        """Запрос создает ответ на комментарий пользователя к своему обращению. Отправляет уведомление на email."""

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

        # try:
        #     send_reply_comment_user_celery.apply_async((
        #         User.objects.get(pk=comment.ticket.user_id).email,
        #         comment.ticket.title,
        #         request.user.first_name,
        #         comment.user_comment,
        #         request.data.get('support_response',''),
        #         frozen,
        #         resolved
        #     ), queue='comments')
        # except OperationalError:
        #     pass
            # print('send reply comment in email error')

        return Response(serializer.data)

