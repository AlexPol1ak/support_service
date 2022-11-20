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
    """Serializer for creating a ticket"""

    class Meta:

        model = Ticket
        fields = ('user_id', 'title', 'user_message',)
        extra_kwargs = {'user_id': {'required': True}}


class GetUsersTiketsSerializer(serializers.ModelSerializer):
    """A serializer for retrieving all the user's tickets."""

    class Meta:

        model = Ticket
        fields = ('id', 'user_id', 'title', 'message_date')


class CommentsSerializer(serializers.ModelSerializer):
    """Serialization of all commentaries"""

    class Meta:

        model = Comments
        fields = '__all__'


class DetailTicketSerializer(serializers.ModelSerializer):
    """Serializer for detailed display of ticket data"""

    # tickets = serializers.StringRelatedField(many=True)
    comments = CommentsSerializer(many=True, read_only=True)
    class Meta:

        model = Ticket
        fields = ['user_id', 'title', 'user_message', 'message_date', 'support_id', 'support_response',
                  'reply_date', 'frozen', 'resolved', 'resolved_date', 'comments']


class CreateCommentSerializer(serializers.ModelSerializer):
    """Serializer for creating user comments to a ticket."""

    ticket_id = serializers.IntegerField(write_only=True)
    class Meta:

        model = Comments
        fields = ('ticket_id', 'user_comment')

    def validate_ticket_id(self, value):
        try:
            ticket = Ticket.objects.get(id=value)
        except:
            raise serializers.ValidationError(f"Ticket {value} not found")

        if self.context['request'].user.pk == ticket.user_id:
            return value
        else:
            raise serializers.ValidationError(f"The user is not the author of the appeal and can not leave comments")


class GetAllTicketsSerializer(serializers.ModelSerializer):
    """Serializer to display all tickets."""

    class Meta:
        model = Ticket
        fields = ['user_id', 'title', 'message_date', 'support_id',
                  'frozen', 'resolved', 'resolved_date',
                  ]


class ReplyTicketSerializer(serializers.ModelSerializer):
    """Serializer for support response to the ticket."""

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
    """A serializer to respond to a comment."""

    support_response = serializers.CharField(min_length=5, max_length=500)
    frozen = serializers.BooleanField(required=False)
    resolved = serializers.BooleanField(required=False)

    class Meta:
        model = Comments
        fields = "__all__"
        read_only_fields = ['user_comment', 'comment_date', 'reply_date', 'support_id', 'ticket',]