"""PDF Viewer view"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from tasks.models import Upload, PDFInfo, VoiceComment
from django.http import JsonResponse
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
        #the below field is just a test field, replace this later on
        list_of_comments  = request.POST.get('listOfComments')
        upload =Upload.objects.filter(id=upload_id)
        if upload.exists():
            mark = PDFInfo.objects.filter(upload=Upload.objects.get(id=upload_id))
            if mark.exists():
                testMark = PDFInfo.objects.get(upload = Upload.objects.get(id=upload_id))
                #update values
                testMark.listOfSpans = listOfSpans
                testMark.mark_id = mark_id
                testMark.listOfComments = list_of_comments
                testMark.save()
            else:
                pdfMark = PDFInfo.objects.create(upload =Upload.objects.get(id=upload_id), listOfSpans=listOfSpans, mark_id = mark_id, listOfComments = list_of_comments)
    return JsonResponse({})

def save_pdf_comments(request):
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