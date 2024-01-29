from django.contrib import admin
from .models import User, Upload
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
        'uploaded_at', 'owner'
    ]