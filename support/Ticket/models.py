from django.core.validators import MinLengthValidator
from django.db import models


class Ticket(models.Model):
    """The model of a user's call to support."""

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

    def __str__(self):
        st = f"User- {self.user_id}.Frozen: {self.frozen}. Resolved: {self.resolved}"
        return st

    class Meta:
        ordering = ['message_date']


class Comments(models.Model):
    """Model of comments on a ticket."""

    user_comment = models.TextField(max_length=500,validators=[MinLengthValidator(4)])
    comment_date = models.DateTimeField(auto_now_add=True)
    support_response = models.TextField(max_length=500, blank=True, validators=[MinLengthValidator(4)])
    reply_date = models.DateTimeField(null=True)
    support_id = models.IntegerField(null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return str(self.ticket)

    class Meta:
        ordering = ['comment_date']





