# Generated by Django 5.1.7 on 2025-05-28 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_rename_date_uploadfiles_last_changes_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.IntegerField()),
                ('text', models.TextField()),
            ],
        ),
    ]
