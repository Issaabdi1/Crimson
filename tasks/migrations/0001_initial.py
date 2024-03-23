# Generated by Django 4.2.6 on 2024-03-23 23:14

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import task_manager.storage_backends
import tasks.models.profile_image
import tasks.models.upload
import tasks.models.voice_comment
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Username must consist of @ followed by at least three alphanumericals', regex='^@\\w{3,}$')])),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('avatar_url', models.TextField(default='https://mypdfbucket01.s3.eu-west-2.amazonaws.com/media/profile_image/default_image.png')),
                ('theme_preference', models.CharField(default='default-mode', max_length=30)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(storage=task_manager.storage_backends.MediaStorage(), upload_to=tasks.models.upload.user_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'], message='Only files with the extension .pdf are supported.')])),
                ('comments', models.TextField(blank=True, default='', null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='VoiceComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark_id', models.IntegerField(null=True)),
                ('audio', models.FileField(upload_to=tasks.models.voice_comment.user_directory_path)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('transcript', models.TextField(blank=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.upload')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('invitation_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('shared_uploads', models.ManyToManyField(to='tasks.upload')),
            ],
        ),
        migrations.CreateModel(
            name='SharedFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shared_date', models.DateTimeField(auto_now_add=True)),
                ('shared_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by', to=settings.AUTH_USER_MODEL)),
                ('shared_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.upload')),
                ('shared_to', models.ManyToManyField(blank=True, related_name='to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=tasks.models.profile_image.user_directory_path)),
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
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_notification', models.DateTimeField()),
                ('read', models.BooleanField(default=False)),
                ('notification_message', models.TextField()),
                ('shared_file_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.sharedfiles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark_id', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('resolved', models.BooleanField(default=False)),
                ('commenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.upload')),
            ],
        ),
    ]
