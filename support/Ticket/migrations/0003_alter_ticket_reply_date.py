# Generated by Django 4.1.3 on 2022-11-13 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ticket', '0002_alter_ticket_resolved_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='reply_date',
            field=models.DateTimeField(null=True),
        ),
    ]
