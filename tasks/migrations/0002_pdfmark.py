# Generated by Django 4.2.6 on 2024-03-05 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listOfMarks', models.JSONField()),
                ('listOfSpans', models.JSONField()),
                ('markId', models.IntegerField()),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.upload')),
            ],
        ),
    ]
