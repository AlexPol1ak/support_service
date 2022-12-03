from Ticket.service import send_reply_user, send_reply_comment_user
from celery_work.celery import app
from celery import shared_task

# docker run --rm -d -p 6379:6379 --name re  redis


#celery -A celery_work worker -n worker.send_mail -Q comments,ticket -l info -P eventlet
#celery --broker=redis://localhost:6379/0 flower
#celery --broker=redis://localhost:6379/0 flower --basic_auth=user1:password1,user2:12345


@app.task(name='reply_ticket')
def send_email_user_celery(*args, **kwargs):
    res = send_reply_user(*args, **kwargs)
    return res

@app.task(name='reply_comment')
def send_reply_comment_user_celery(*args, **kwargs):
    res = send_reply_comment_user(*args, **kwargs)
    return res

