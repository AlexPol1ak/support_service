from django.core.validators import MinLengthValidator
from django.db import models

class Ticket(models.Model):
    user_id = models.IntegerField() # automatically in the user serializer
    title = models.CharField(max_length=45 ,validators=[MinLengthValidator(4)])
    user_message = models.TextField(max_length=500, validators=[MinLengthValidator(4)])
    message_date = models.DateTimeField(auto_now_add=True)
    support_id = models.IntegerField(null=True) # automatically in the support serializer
    support_response = models.TextField(max_length=500, blank=True)
    reply_date = models.DateTimeField(null=True)
    frozen = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    resolved_date = models.DateTimeField(null=True) # automatically in the support serializer
    is_comment = models.BooleanField(default=False) # automatically in the support serializer

    def __str__(self):
        st = f"User- {self.user_id}.Frozen: {self.frozen}. Resolved: {self.resolved}"
        return st

# from Ticket.models import *
# t = Ticket.objects.create(user_id=4, title="new title", user_message='new message')

class Comments(models.Model):
    user_comment = models.TextField(max_length=500,validators=[MinLengthValidator(4)])
    comment_date = models.DateTimeField(auto_now_add=True)
    support_response = models.TextField(max_length=500, blank=True, validators=[MinLengthValidator(4)])
    reply_date = models.DateTimeField(null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ticket)





