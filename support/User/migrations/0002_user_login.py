# Generated by Django 4.1.3 on 2022-11-03 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login',
            field=models.EmailField(default=0, max_length=40, unique=True),
            preserve_default=False,
        ),
    ]
