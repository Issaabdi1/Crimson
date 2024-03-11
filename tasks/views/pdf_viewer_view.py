"""PDF Viewer view"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from tasks.models import Upload, PDFInfo
from django.http import JsonResponse
from django.forms.models import model_to_dict

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
                    context['voice_comments'] = mark.comments.all()
                    print("List of omments is ", mark.listOfComments)

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
