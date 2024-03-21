from django.contrib import admin
from .models import User, Upload, Team, ProfileImage, SharedFiles, Notification, PDFInfo, VoiceComment
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'avatar_url'
    ]


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for uploads"""
    list_display = [
        'uploaded_at', 'owner', 'file'
    ]


@admin.register(Team)
class UploadAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for teams"""
    list_display = [
        'name', 'invitation_code'
    ]

@admin.register(ProfileImage)
class UploadAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for ProfileImages"""
    list_display = [
        'user'
    ]

@admin.register(SharedFiles)
class SharedFilesAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for SharedFiles"""
    list_display = [
        'shared_file', 'shared_by', 'shared_date'
    ]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Notifications"""
    list_display = [
        'shared_file_instance', 'user', 'time_of_notification', 'notification_message'
    ]

@admin.register(PDFInfo)
class PDFInfoAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for PDFInfo"""
    list_display = [
        'upload', 'mark_id'
    ]

@admin.register(VoiceComment)
class VoiceCommentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for VoiceComment"""
    list_display = [
        'user', 'upload', 'mark_id'
    ]