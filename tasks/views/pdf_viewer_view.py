"""PDF Viewer view"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from tasks.models import Upload, PDFInfo, VoiceComment
from django.http import JsonResponse
from django.utils import timezone
from tasks.models import Comment
from django.forms.models import model_to_dict
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64, json, uuid


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
                if(PDFInfo.objects.filter(upload=upload).exists()):
                    #get the mark instance
                    context['marks'] = PDFInfo.objects.get(upload = upload)
                    mark = PDFInfo.objects.get(upload = upload)

                    # Generate saved comments dictionary
                    allVoiceComments = VoiceComment.objects.filter(upload=upload)
                    listOfSavedComments = {}
                    if allVoiceComments:
                        for vc in allVoiceComments:
                            if vc.mark_id not in listOfSavedComments:
                                listOfSavedComments[vc.mark_id] = []
                            listOfSavedComments[vc.mark_id].append(vc.audio.url)
                        context['listOfSavedComments'] = json.dumps(listOfSavedComments)
                comments = Comment.objects.filter(upload=upload)
                context['comments'] = comments
                if (PDFInfo.objects.filter(upload=upload).exists()):
                    # get the mark instance
                    context['marks'] = PDFInfo.objects.get(upload=upload)
                    mark = PDFInfo.objects.get(upload=upload)
                    print("List of comments is ", mark.listOfComments)

            except Upload.DoesNotExist:
                messages.add_message(request, messages.ERROR, "Upload does not exist!")
        else:
            messages.add_message(request, messages.ERROR, f'Upload id was not specified in the form!')

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

def save_pdf_comments(request):
    """Saves the voice comments added to each mark on the PDF"""
    if request.method == "POST":
        voice_comment_str = request.POST.get('voice-comment-list')
        voice_comment_list = json.loads(voice_comment_str)
        upload_id = request.POST.get('upload_id')
        upload = Upload.objects.get(id=upload_id)
        user = request.user
        if upload and voice_comment_list:
            for mark_id in voice_comment_list:
                for voice_comment in voice_comment_list[mark_id]:
                    filename = f"{uuid.uuid4()}.wav"
                    voice_comment_decode = base64.b64decode(voice_comment)
                    audio_file = ContentFile(voice_comment_decode, name=filename)
                    VoiceComment.objects.create(
                        user=user,
                        upload=upload,
                        mark_id=mark_id,
                        audio=audio_file,
                    )
            vc = VoiceComment.objects.all()
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
                except e:
                    return JsonResponse({}, status=500)
                voice_comment.audio.delete()
                voice_comment.delete()
    return JsonResponse({})
def save_comment(request):
    if request.method == "POST":
        comment_text = request.POST.get('comments')
        mark_id = request.POST.get('mark_id')
        upload_id = request.POST.get('upload_id')
        commenter = request.user

        now = timezone.now()
        Comment.objects.create(
            upload_id=upload_id,
            mark_id=mark_id,
            commenter=commenter,
            date=now,
            text=comment_text,
        )
        all_comments = Comment.objects.all()

        print(all_comments)

        return render(request, 'viewer.html', {'all_comments': all_comments})
    else:
        return JsonResponse({"success": False, "error": "Only POST requests are allowed"})



