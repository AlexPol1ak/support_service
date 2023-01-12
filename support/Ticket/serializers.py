from datetime import datetime

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from Ticket.models import Comments, Ticket

# Alternative option
# class CreateTicketSerializer(serializers.ModelSerializer):
#       """Serializer for creating a ticket"""
#
#     class Meta:
#         model = Ticket
#         fields = ('title', 'user_message',)
#
#     def create(self, validated_data):
#         ticket = Ticket(
#             user_id=self.context['request'].user.pk ,
#             title=validated_data['title'],
#             user_message=validated_data['user_message']
#         )
#         ticket.save()
#
#         return ticket


class CreateTicketSerializer(serializers.ModelSerializer):
    """Сериализатор для создания обращения. """

    class Meta:

        model = Ticket
        fields = ('user_id', 'title', 'user_message',)
        extra_kwargs = {'user_id': {'required': True}}


class GetUsersTiketsSerializer(serializers.ModelSerializer):
    """Сериализатор для получения всех обращений пользователя."""

    class Meta:

        model = Ticket
        fields = ('id', 'user_id', 'title', 'message_date')


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для получения всех комментариев."""

    class Meta:

        model = Comments
        fields = '__all__'


class DetailTicketSerializer(serializers.ModelSerializer):
    """Сериализатор для детального отображения одного обращения."""

    # tickets = serializers.StringRelatedField(many=True)
    comments = CommentsSerializer(many=True, read_only=True)
    class Meta:

        model = Ticket
        fields = ['user_id', 'title', 'user_message', 'message_date', 'support_id', 'support_response',
                  'reply_date', 'frozen', 'resolved', 'resolved_date', 'comments']


class CreateCommentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователем комментария."""

    ticket_id = serializers.IntegerField(write_only=True)
    class Meta:

        model = Comments
        fields = ('ticket_id', 'user_comment')

    def validate_ticket_id(self, value):
        """Проверяет совпадения id пользователя с id автора обращения. """
        try:
            ticket = Ticket.objects.get(id=value)
        except:
            raise serializers.ValidationError(f"Ticket {value} not found")

        if self.context['request'].user.pk == ticket.user_id:
            return value
        else:
            raise serializers.ValidationError(f"The user is not the author of the appeal and can not leave comments")


class GetAllTicketsSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения всех обращений."""

    class Meta:
        model = Ticket
        fields = ['user_id', 'title', 'message_date', 'support_id',
                  'frozen', 'resolved', 'resolved_date',
                  ]


class ReplyTicketSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа агента поддержки на обращение пользователя."""

    frozen = serializers.BooleanField(default=False,)
    resolved = serializers.BooleanField(default=False,)

    class Meta:
        model = Ticket
        fields = ['support_id', 'support_response', 'reply_date', 'frozen', 'resolved', 'resolved_date']
        extra_kwargs = {'user_id': {'read_only': True},
                        'resolved_date': {'read_only': True},
                        'reply_date': {'read_only': True},
                        }


class ReplyCommentSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа агента поддержки на комментарий пользователя к обращению."""

    support_response = serializers.CharField(min_length=5, max_length=500)
    frozen = serializers.BooleanField(required=False)
    resolved = serializers.BooleanField(required=False)

    class Meta:
        model = Comments
        fields = "__all__"
        read_only_fields = ['user_comment', 'comment_date', 'reply_date', 'support_id', 'ticket',]