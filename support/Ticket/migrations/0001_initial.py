# Generated by Django 4.1.3 on 2022-11-13 20:00

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('title', models.CharField(max_length=45, validators=[django.core.validators.MinLengthValidator(4)])),
                ('user_message', models.TextField(max_length=500, validators=[django.core.validators.MinLengthValidator(4)])),
                ('message_date', models.DateTimeField(auto_now_add=True)),
                ('support_id', models.IntegerField(null=True)),
                ('support_response', models.TextField(blank=True, max_length=500)),
                ('reply_date', models.DateTimeField(auto_now=True)),
                ('frozen', models.BooleanField(default=False)),
                ('resolved', models.BooleanField(default=False)),
                ('resolved_date', models.DateTimeField(blank=True)),
                ('is_comment', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_comment', models.TextField(max_length=500, validators=[django.core.validators.MinLengthValidator(4)])),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('support_response', models.TextField(max_length=500, validators=[django.core.validators.MinLengthValidator(4)])),
                ('reply_date', models.DateTimeField(auto_now=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ticket.ticket')),
            ],
        ),
    ]
