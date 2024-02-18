from django.contrib import admin
from .models import User, Upload, Team, VoiceComment
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""
    list_display = [
        'username', 'first_name', 'last_name', 'email'
    ]


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for uploads"""
    list_display = [
        'id','uploaded_at', 'owner'
    ]


@admin.register(Team)
class UploadAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for teams"""
    list_display = [
        'name',
    ]

@admin.register(VoiceComment)
class VoiceCommentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for uploads"""
    list_display = [
        'uploaded_at', 'owner','get_sound_file_path','upload'
    ]