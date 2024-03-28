"""PDF Viewer view"""
from venv import logger

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.timesince import timesince
from tasks.models import Comment
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from tasks.models import Upload, PDFInfo, VoiceComment, Notification, SharedFiles, Team
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64, json, uuid
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@login_required
def viewer(request):
    """Displays the PDF in the custom PDF viewer"""

    context = {}
    if request.method == "POST":
        upload_id = request.POST.get('upload_id')
        # Check if the 'upload_id' is present in the form data
        if upload_id is not None:
            try:
                upload = Upload.objects.get(id=upload_id)
                context['upload'] = upload
                if (PDFInfo.objects.filter(upload=upload).exists()):
                    # get the mark instance
                    context['marks'] = PDFInfo.objects.get(upload=upload)
                    mark = PDFInfo.objects.get(upload=upload)
                    print("List of omments is ", mark.listOfComments)
                    # Generate saved comments dictionary (2D Dictionary)
                    # outer key is mark ID inner key is user)
                    allVoiceComments = VoiceComment.objects.filter(upload=upload)
                    listOfSavedComments = {}
                    if allVoiceComments:
                        for vc in allVoiceComments:
                            mark_id = vc.mark_id
                            if mark_id not in listOfSavedComments:
                                listOfSavedComments[mark_id] = []
                            listOfSavedComments[mark_id].append({
                                'username': vc.user.username,
                                'avatar_url': vc.user.avatar_url,
                                'audio_url': vc.audio.url,
                                'transcript': vc.transcript,
                                'time_ago': timesince(vc.timestamp) + ' ago',
                                'is_resolved': vc.is_resolved
                            })
                        context['listOfSavedComments'] = json.dumps(listOfSavedComments)
            except Upload.DoesNotExist:
                messages.add_message(request, messages.ERROR, "Upload does not exist!")
        else:
            messages.add_message(request, messages.ERROR, f'Upload id was not specified in the form!')
    context['current_user'] = request.user

    return render(request, 'viewer.html', context)


def save_pdf_info(request):
    """Saves the information added to the PDF"""
    if request.method == "POST":
        listOfSpans = request.POST.get('listOfSpans')
        upload_id = request.POST.get('upload_id')
        mark_id = request.POST.get('mark_id')
        list_of_comments = request.POST.get('listOfComments')
        upload = Upload.objects.filter(id=upload_id)
        if upload.exists():
            mark = PDFInfo.objects.filter(upload=Upload.objects.get(id=upload_id))
            if mark.exists():
                existingMark = PDFInfo.objects.get(upload=Upload.objects.get(id=upload_id))
                # Update values for existing mark
                existingMark.listOfSpans = listOfSpans
                existingMark.mark_id = mark_id
                existingMark.listOfComments = list_of_comments
                existingMark.save()
            else:
                # Create a new mark
                pdfMark = PDFInfo.objects.create(upload=Upload.objects.get(id=upload_id), listOfSpans=listOfSpans,
                                                 mark_id=mark_id, listOfComments=list_of_comments)
    return JsonResponse({})


def save_voice_comments(request):
    """Saves the voice comments added to each mark on the PDF"""
    if request.method == "POST":
        voice_comment_str = request.POST.get('voice-comment-list')

        try:
            voice_comment_list = json.loads(voice_comment_str)
        except Exception as e:
            return JsonResponse({}, status=400)

        upload_id = request.POST.get('upload_id')
        upload = Upload.objects.get(id=upload_id)
        user = request.user
        if upload and voice_comment_list:
            saved_comments = {}
            for mark_id in voice_comment_list:
                for voice_comment_data in voice_comment_list[mark_id]:
                    voice_comment = voice_comment_data.get("blob")
                    transcript = voice_comment_data.get("transcript", "")
                    filename = f"{uuid.uuid4()}.wav"
                    voice_comment_decode = base64.b64decode(voice_comment)
                    audio_file = ContentFile(voice_comment_decode, name=filename)
                    saved_comment = VoiceComment.objects.create(
                        user=user,
                        upload=upload,
                        mark_id=mark_id,
                        audio=audio_file,
                        transcript=transcript
                    )
                    if mark_id not in saved_comments:
                        saved_comments[mark_id] = []
                    saved_comments[mark_id].append({
                        'username': saved_comment.user.username,
                        'avatar_url': saved_comment.user.avatar_url,
                        'audio_url': saved_comment.audio.url,
                        'transcript': saved_comment.transcript,
                        'time_ago': timesince(saved_comment.timestamp) + ' ago',
                        'is_resolved': saved_comment.is_resolved,
                    })
                    teams = upload.get_teams()#get all teams
                    for team in teams:
                        for member in team.members.all():
                            if(member!=user):
                                Notification.objects.create(
                                    upload=saved_comment.upload,
                                    shared_file_instance=None,
                                    user=user,
                                    time_of_notification=timezone.now(),
                                    notification_message=f'{request.user} recorded a voice comment'
                                )
                    #If this file has been shared to a user or a team
                    #currentTeam = Team.objects.filter(shared_uploads=shared_file in shared_uploads)
                    #Check for a team
                    if SharedFiles.objects.filter(shared_file=saved_comment.upload).exists():
                        # Create a notification for everyone else who was shared this file
                        shared_file = SharedFiles.objects.get(shared_file=saved_comment.upload)
                        list_of_users= list(shared_file.shared_to.all())
                        list_of_users.append(shared_file.shared_by)
                        for user in list_of_users:
                            if user!=request.user:
                                # Create a new notification to tell them the comment was created
                                Notification.objects.create(
                                    upload=saved_comment.upload,
                                    shared_file_instance=shared_file,
                                    user=user,
                                    time_of_notification=timezone.now(),
                                    notification_message=f'{request.user} recorded a voice comment'
                                )
            return JsonResponse({'recentlySavedComments': saved_comments})
        else:
            return JsonResponse({}, status=404)
    return JsonResponse({})


def delete_voice_comment(request):
    if request.method == "POST":
        audio_url = request.POST.get('audio-url')
        if audio_url is not None:
            voice_comment = None
            for vc in VoiceComment.objects.all():
                if audio_url == vc.audio.url:
                    voice_comment = vc
                    break
            if voice_comment is not None:
                try:
                    default_storage.delete(voice_comment.audio.name)
                except Exception as e:
                    return JsonResponse({}, status=500)
                voice_comment.audio.delete()
                voice_comment.delete()
            else:
                return JsonResponse({}, status=404)
    return JsonResponse({})

def mark_as_resolved(request):
    if request.method == "POST":
        audio_url = request.POST.get('audio_url')
        if audio_url is not None:
            voice_comment = None
            for vc in VoiceComment.objects.all():
                if audio_url == vc.audio.url:
                    voice_comment = vc
                    break
            if voice_comment is not None:
                voice_comment.is_resolved = True
                voice_comment.save()
                teams = voice_comment.upload.get_teams()#get all teams
                for team in teams:
                    for member in team.members.all():
                        if(member!=request.user):
                            Notification.objects.create(
                                upload=voice_comment.upload,
                                shared_file_instance=None,
                                user=member,
                                time_of_notification=timezone.now(),
                                notification_message=f'{request.user} resolved a comment'
                            )
                #If this file has been shared to a user or a team
                #Check for a team
                if SharedFiles.objects.filter(shared_file=voice_comment.upload).exists():
                    # Create a notification for everyone else who was shared this file (and the owner)
                    shared_file = SharedFiles.objects.get(shared_file=voice_comment.upload)
                    list_of_users= list(shared_file.shared_to.all())
                    list_of_users.append(shared_file.shared_by)
                    for user in list_of_users:
                        if user!=request.user:
                            # Create a new notification to tell them the comment was resolved
                            Notification.objects.create(
                                upload=voice_comment.upload,
                                shared_file_instance=shared_file,
                                user=user,
                                time_of_notification=timezone.now(),
                                notification_message=f'{request.user} resolved a comment'
                            )
    return JsonResponse({})

def save_comment(request):
    if request.method == "POST":
        mark_id = request.POST.get('mark_id')
        upload_id = request.POST.get('upload_id')
        commenter = request.user
        text = request.POST.get('text')
        now = timezone.now()

        upload = Upload.objects.get(id=upload_id)
        comment = Comment.objects.create(
            upload=upload,
            mark_id=mark_id,
            commenter=commenter,
            date=now,
            text=text,
        )
        comments = Comment.objects.filter(mark_id=mark_id, upload=upload)
        teams = upload.get_teams()#get all teams
        for team in teams:
            for member in team.members.all():
                if(member!=request.user):
                    Notification.objects.create(
                        upload=upload,
                        shared_file_instance=None,
                        user=member,
                        time_of_notification=timezone.now(),
                        notification_message=f'{request.user} added a comment'
                    )
        if SharedFiles.objects.filter(shared_file=upload).exists():
            # Create a notification for everyone else who was shared this file
            shared_file = SharedFiles.objects.get(shared_file=upload)
            list_of_users= list(shared_file.shared_to.all())
            list_of_users.append(shared_file.shared_by)
            for user in list_of_users:
                if user!=request.user:
                    # Create a new notification to tell them the comment was resolved
                    Notification.objects.create(
                        upload=upload,
                        shared_file_instance=shared_file,
                        user=user,
                        time_of_notification=timezone.now(),
                        notification_message=f'{request.user} added a comment'
                    )
        return render(request, 'viewer.html', {'comments': comments, 'current_mark_id': mark_id})
    else:
        return JsonResponse({"success": False, "error": "Only POST requests are allowed"})


@require_POST
def clear_comment(request):
    Comment.objects.all().delete()
    return HttpResponse(status=204)


def get_comments(request):
    if request.method == "GET":
        upload_id = request.GET.get('upload_id')
        mark_id = request.GET.get('mark_id')
        if upload_id is not None and mark_id is not None:
            try:
                upload = get_object_or_404(Upload, pk=upload_id)
                comments = Comment.objects.filter(upload=upload, mark_id=mark_id)
                comments_json = json.dumps([{
                    'commenter': comment.commenter.username,
                    'avatar_url': comment.commenter.avatar_url,
                    'text': comment.text,
                    'comment_id': comment.id,
                    'date': comment.formatted_date(),
                    'resolved': comment.resolved,
                } for comment in comments])
                return JsonResponse({"comments": comments_json})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "Upload ID or Mark ID not provided"}, status=400)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)


def save_current_mark_id(request):
    if request.method == 'POST':
        mark_id = request.POST.get('mark_id')
        context = {'current_mark_id': mark_id}
        return render(request, 'viewer.html', context)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@require_POST
def update_comment(request):
    data = json.loads(request.body)
    comment_id = data.get('comment_id')
    new_text = data.get('text')
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.text = new_text
        comment.save()
        return JsonResponse({'success': True, 'message': 'Comment updated successfully'})
    except Comment.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Comment not found'}, status=404)
    except Comment.MultipleObjectsReturned:
        return JsonResponse({'success': False, 'message': 'Multiple comments found'}, status=400)


@require_POST
@csrf_exempt
def delete_text_comment(request):
    data = json.loads(request.body)
    comment_id = data.get('id')

    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return JsonResponse({'status': 'success', 'message': 'Comment deleted successfully'})


def get_comments_json(request, upload_id, mark_id):
    comments = Comment.objects.filter(upload_id=upload_id, mark_id=mark_id)
    comments_data = list(comments.values(
        "id", "text", "commenter_id",
        "commenter", "resolved",
    ))
    return JsonResponse({"comments": comments_data})

@require_POST
def update_comment_status(request):
    # Check for the correct content type
    if request.content_type != 'application/json':
        return JsonResponse({'error': 'Invalid content type'}, status=400)

    try:
        data = json.loads(request.body)
        comment_id = data.get('comment_id')
        upload_id = data.get('upload_id')
        resolved = data.get('resolved')
        comment = Comment.objects.get(id=comment_id)
        comment.resolved = resolved
        comment.save()
        upload = get_object_or_404(Upload, pk=upload_id)
        #Create notifications for teams
        teams = upload.get_teams()#get all teams
        for team in teams:
            for member in team.members.all():
                if(member!=request.user):
                    Notification.objects.create(
                        upload=upload,
                        shared_file_instance=None,
                        user=member,
                        time_of_notification=timezone.now(),
                        notification_message=f'{request.user} added a comment'
                    )
        # Create a notification for everyone else who was shared this file, including the owner
        if upload.sharedfiles_set.count() > 0:
            shared_file = SharedFiles.objects.get(shared_file=upload)
            list_of_users= list(shared_file.shared_to.all())
            list_of_users.append(shared_file.shared_by)
            for user in list_of_users:
                if user!=request.user:
                    # Create a new notification to tell them the comment was resolved
                    Notification.objects.create(
                        upload=upload,
                        shared_file_instance=shared_file,
                        user=user,
                        time_of_notification=timezone.now(),
                        notification_message=f'{request.user} resolved a comment'
                    )
        return JsonResponse({"success": True, "message": "Comment status updated successfully."})
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON or empty payload'}, status=400)
    except Comment.DoesNotExist:
        # Handle case where comment does not exist
        return JsonResponse({'error': 'Comment not found'}, status=404)