"""PDF Viewer view"""
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone
from tasks.models import Comment
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from tasks.models import Upload, PDFInfo, VoiceComment
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64, json, uuid
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
                            if vc.mark_id not in listOfSavedComments:
                                listOfSavedComments[vc.mark_id] = {}
                            username = vc.user.username
                            if username not in listOfSavedComments[vc.mark_id]:
                                listOfSavedComments[vc.mark_id][username] = []
                            listOfSavedComments[vc.mark_id][username].append(vc.audio.url)
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
        # the below field is just a test field, replace this later on
        list_of_comments = request.POST.get('listOfComments')
        upload = Upload.objects.filter(id=upload_id)
        if upload.exists():
            mark = PDFInfo.objects.filter(upload=Upload.objects.get(id=upload_id))
            if mark.exists():
                testMark = PDFInfo.objects.get(upload=Upload.objects.get(id=upload_id))
                # update values
                testMark.listOfSpans = listOfSpans
                testMark.mark_id = mark_id
                testMark.listOfComments = list_of_comments
                testMark.save()
            else:
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
            for mark_id in voice_comment_list:
                for voice_comment_data in voice_comment_list[mark_id]:
                    print(voice_comment_data)
                    voice_comment = voice_comment_data.get("blob")
                    transcript = voice_comment_data.get("transcript", "")
                    filename = f"{uuid.uuid4()}.wav"
                    voice_comment_decode = base64.b64decode(voice_comment)
                    audio_file = ContentFile(voice_comment_decode, name=filename)
                    VoiceComment.objects.create(
                        user=user,
                        upload=upload,
                        mark_id=mark_id,
                        audio=audio_file,
                    )
                    if transcript:
                        Comment.objects.create(
                            upload_id=upload_id,
                            mark_id=mark_id,
                            commenter=request.user,
                            date=timezone.now(),
                            text=transcript
                        )
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


def save_comment(request):
    if request.method == "POST":
        mark_id = request.POST.get('mark_id')
        upload_id = request.POST.get('upload_id')
        commenter = request.user
        text = request.POST.get('text')
        now = timezone.now()
        Comment.objects.create(
            upload_id=upload_id,
            mark_id=mark_id,
            commenter=commenter,
            date=now,
            text=text,
        )
        comments = Comment.objects.filter(mark_id=mark_id, upload_id=upload_id)

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
        comments = Comment.objects.filter(upload_id=upload_id, mark_id=mark_id)
        comments_json = json.dumps([{
            'commenter': comment.commenter.username,
            'avatar_url': comment.commenter.avatar_url,
            'text': comment.text,
        } for comment in comments])
        print(comments_json)

        print('the upload id you get is:', upload_id)
        print('the mark id you get is:', mark_id)

        if upload_id is not None and mark_id is not None:
            try:
                upload = get_object_or_404(Upload, pk=upload_id)
                comments = Comment.objects.filter(upload=upload, mark_id=mark_id)
                print(comments)
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
        # print('This is mark id in save current mark id:'+mark_id)
        # print("This is the request post of save current mark id:", request.POST)
        context = {'current_mark_id': mark_id}

        return render(request, 'viewer.html', context)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def update_comment(request):
    if request.method == 'POST':
        mark_id = request.POST.get('mark_id')
        upload_id = request.POST.get('upload_id')
        new_text = request.POST.get('text')
        print('the new text is', new_text)
        print('mark_id is', mark_id)
        print('upload_id is', upload_id)

        try:
            comment = Comment.objects.get(mark_id=mark_id, upload_id=upload_id)
            comment.text = new_text
            comment.save()
            return JsonResponse({'success': True, 'message': 'Comment updated successfully'})
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Comment not found'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
