import time

from Ticket.service import send_reply_user, send_reply_comment_user
from celery_work.celery import app
from celery import shared_task

# docker run --rm -d -p 6379:6379 --name re  redis



#celery -A celery_work worker -n worker.send_mail -Q comments,ticket -l info -P eventlet
#celery --broker=redis://localhost:6379/0 flower
#celery --broker=redis://redis:6379/0 flower
#celery --broker=redis://localhost:6379/0 flower --basic_auth=user1:password1,user2:12345

#    command:

#       - python manage.py runserver 0.0.0.0:8000
#       - celery -A celery_work worker -n worker.send_mail -Q comments,ticket -l info -P eventlet
#       - celery --broker=${REDIS_PREFIX}${REDIS_HOST}:${REDIS_PORT}/0 flower --basic_auth=${FLOWER_LOGIN}:${FLOWER_PASSWORD}


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

