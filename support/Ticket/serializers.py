from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from Ticket.models import Ticket



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


class GetUsersTiketsSerializer(serializers.ModelSerializer):
    """A serializer for retrieving all of the user's tickets."""
    class Meta:
        model = Ticket
        fields = ('id', 'user_id', 'title', 'user_message', 'message_date')

class DetailTicketSerializer(serializers.ModelSerializer):
    """Serializer for detailed display of ticket data"""
    class Meta:
        model = Ticket
        fields = "__all__"

