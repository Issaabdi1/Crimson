"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.test, name="test"),  #This is a test url for now, should probably change this so only super users can see it
    path('test_viewer_1/', views.test_viewer_1, name="test_viewer_1"),
    path('test_viewer_2/', views.test_viewer_2, name="test_viewer_2"),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('preferences/', views.preferences_view, name = 'preferences'),
    path('profile/', views.profile_update_view, name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('filelist/', views.filelist, name='filelist'),
    path('shared_file_list/', views.shared_file_list, name='shared_file_list'),
    path('share_file/', views.share_file, name='share_file'),
    path('outer_comment_views/<int:upload_id>/', views.outer_comment_views, name='outer_comment_views'),
    path('process_notification_delete/', views.process_notification_delete, name='process_notification_delete'),
    path('set_notifications_as_read/', views.set_notifications_as_read, name='set_notifications_as_read'),
    path('delete_upload/<int:upload_id>/', views.delete_upload, name='delete_upload'),
    path('delete_all_upload/', views.delete_all_upload_views, name='delete_all_upload_views'),
    path('team_list/', views.list_team_view, name='team_list'),
    path('team_detail/<int:team_id>/', views.team_detail_view, name='team_detail'),
    path('unshare_file/<int:upload_id>/<int:user_id>/', views.unshare_file, name='unshare_file'),
    path('filelist/rename/<int:upload_id>/', views.rename_upload_view, name='rename_upload'),
    path('upload_file/', views.upload_file_view, name='upload_file'),
    path('delete_voice_comment/', views.delete_voice_comment, name='delete_voice_comment'),
    path('team_detail/<int:team_id>/leave', views.leave_team_view, name='team_leave'),
    path('download-single/<int:upload_id>/', views.download_single, name='download_single'),
    path('download_multiple/', views.download_multiple, name='download_multiple'),
    path('delete_selected_uploads/', views.delete_selected_uploads, name='delete_selected_uploads'),
    path('pdf_viewer/', views.viewer, name='pdf_viewer'),
    path('save_pdf_marks/', views.save_pdf_info, name='save_pdf_marks'),
    path('save_voice_comments/', views.save_voice_comments, name='save_voice_comments'),
    path('delete_voice_comment/', views.delete_voice_comment, name='delete_voice_comment'),
    path('delete_text_comment/', views.delete_text_comment, name='delete_text_comment'),
    path('save_comment/', views.save_comment, name='save_comment'),
    path('clear_comment/', views.clear_comment, name='clear_comment'),
    path('get_comments/', views.get_comments, name='get_comments'),
    path("save_current_mark_id/", views.save_current_mark_id, name="save_current_mark_id"),
    path('get_comments_json/<int:upload_id>/<int:mark_id>/', views.get_comments_json, name='get_comments_json'),
    path("update_comment/", views.update_comment, name="update_comment"),
    path("update_comment_status/", views.update_comment_status, name="update_comment_status"),
    path("mark_as_resolved/", views.mark_as_resolved, name="mark_as_resolved")
]
