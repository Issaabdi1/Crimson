# Generated by Django 4.2.6 on 2024-02-14 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_upload_sharedfiles_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_message',
            field=models.TextField(default='blank'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]