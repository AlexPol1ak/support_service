
echo "Apply database migrations"
python manage.py migrate

echo "start celery"
celery -A celery_work worker -D -n worker.send_mail -Q comments,ticket -l info -P eventlet

echo "Start server"
gunicorn support.wsgi:application --bind 0.0.0.0:8000














