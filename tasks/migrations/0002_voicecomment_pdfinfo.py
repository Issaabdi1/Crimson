# Generated by Django 4.2.6 on 2024-03-11 21:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tasks.models.voice_comment


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoiceComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark_id', models.IntegerField(null=True)),
                ('audio', models.FileField(upload_to=tasks.models.voice_comment.user_directory_path)),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.upload')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PDFInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listOfSpans', models.JSONField()),
                ('mark_id', models.IntegerField()),
                ('listOfComments', models.JSONField()),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.upload')),
            ],
        ),
    ]