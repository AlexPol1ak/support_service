# Superuser  регистрируется автоматически при запуске приложения через docker.,
# если в переменные среды были переданы соответствующие регистрационные данные.
# Если superuser зарегистрирован в базе данных
# или регистрационные данные не были переданы в переменные среды - superuser не регистрируется.
# Superuser имеет все полномочия службы поддержки, а так же назначать и разжаловать службу поддержки из числа
# зарегистрированных пользователей.


import os

import django
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "support.settings")
django.setup()
load_dotenv()

def create_superuser():
    """Create superuser."""
    # Superuser может назначать и разжаловать пользвателей поддержки.
    from User import models

    s_users = models.User.objects.filter(is_superuser=True)
    if len(s_users) >= 1:
        print('Superuser already registered')
        return False

    login = os.environ.get('ADMIN_LOGIN')
    password = os.environ.get('ADMIN_PASSWORD')
    email = os.environ.get('ADMIN_EMAIL')
    last_name = os.environ.get('ADMIN_LAST_NAME')
    first_name = os.environ.get('ADMIN_FIRST_NAME')

    if login and password and email and last_name and first_name:
        s_user = models.User()

        s_user.login = login
        s_user.set_password(password)
        s_user.email = email
        s_user.last_name = last_name
        s_user.first_name = first_name
        s_user.is_superuser = True
        s_user.is_support = True
        s_user.is_staff = True
        s_user.save()
        print('Superuser created')
        return True
    else:
        print('Credentials for superuser registration are not set.')

create_superuser()
