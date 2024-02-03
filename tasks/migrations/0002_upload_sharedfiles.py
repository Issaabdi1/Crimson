# Generated by Django 4.2.6 on 2024-02-02 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import task_manager.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(storage=task_manager.storage_backends.MediaStorage(), upload_to='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='SharedFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shared_file', models.FileField(storage=task_manager.storage_backends.MediaStorage(), upload_to='')),
                ('shared_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by', to=settings.AUTH_USER_MODEL)),
                ('shared_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
