from Ticket.service import send_email_user
from celery_work.celery import app
from celery import shared_task

# docker run --rm -d -p 6379:6379 --name re  redis
# celery -A celery_work worker -l info -P eventlet

@app.task
def send_email_user_celery(*args, **kwargs):
    res = send_email_user(*args, **kwargs)
    return res

