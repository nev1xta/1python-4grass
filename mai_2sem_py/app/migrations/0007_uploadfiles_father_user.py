# Generated by Django 5.1.7 on 2025-04-11 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_uploadfiles_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfiles',
            name='father_user',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
