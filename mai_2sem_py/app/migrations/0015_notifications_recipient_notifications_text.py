# Generated by Django 5.1.7 on 2025-05-28 23:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_notifications_recipient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='recipient',
            field=models.IntegerField(default=datetime.datetime(2025, 5, 29, 2, 1, 47, 435478)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notifications',
            name='text',
            field=models.TextField(default='a'),
            preserve_default=False,
        ),
    ]
