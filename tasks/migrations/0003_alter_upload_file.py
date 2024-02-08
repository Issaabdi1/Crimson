# Generated by Django 4.2.6 on 2024-02-07 11:36

import django.core.validators
from django.db import migrations, models
import task_manager.storage_backends
import tasks.models.upload


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_upload_sharedfiles_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='file',
            field=models.FileField(storage=task_manager.storage_backends.MediaStorage(), upload_to=tasks.models.upload.user_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'], message='Only files with the extension .pdf are supported.')]),
        ),
    ]
