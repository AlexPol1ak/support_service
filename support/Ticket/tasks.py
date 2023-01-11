from celery import shared_task

from celery_work.celery import app
from Ticket.service import send_reply_comment_user, send_reply_user


@app.task(bind=True,name='reply_ticket')
def send_email_user_celery(self, *args, **kwargs):

    try:
        res = send_reply_user(*args, **kwargs)
    except Exception as e:
        raise self.retry(exc=e, countdown=300)

    return res

@app.task(bind=True, name='reply_comment',)
def send_reply_comment_user_celery(self, *args, **kwargs):
    try:
        res = send_reply_comment_user(*args, **kwargs)
    except Exception as e:
        raise self.retry(exc=e, countdown=300)

    return res

