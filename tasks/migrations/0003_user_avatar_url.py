# Generated by Django 4.2.6 on 2024-03-12 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_user_theme_preference'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_url',
            field=models.TextField(default='https://mypdfbucket01.s3.eu-west-2.amazonaws.com/media/profile_image/default_image.png'),
        ),
    ]
