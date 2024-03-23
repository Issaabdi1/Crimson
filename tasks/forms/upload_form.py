"""Upload File Forms for the app."""
from django import forms
from tasks.models import Upload


class FileForm(forms.Form):
    file = forms.FileField(
        label='Select a File',
        help_text='only files with the extension .pdf are supported, maximum file size allowed is 100 MB.',
        label_suffix=''
    )
    user = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, file):
        """Save the uploaded file."""

        upload = Upload(file=file, owner=self.user)
        upload.full_clean()
        upload.save()
        return upload


class RenameForm(forms.Form):
    new_name = forms.CharField(label='New file name')
