"""Unit tests of the file form."""
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from tasks.forms import FileForm
from tasks.models import User, Upload

class FileFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.file = SimpleUploadedFile(f'test_file_form.pdf', b'file form test')

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()

    def test_form_has_necessary_fields(self):
        form = FileForm()
        self.assertIn('file', form.fields)
        file_field = form.fields['file']
        self.assertTrue(isinstance(file_field, forms.FileField))

    def test_form_must_save_correctly(self):
        user = User.objects.get(username='@johndoe')
        form = FileForm()
        form.user = user
        before_count = Upload.objects.count()
        form.save(self.file)
        after_count = Upload.objects.count()
        self.assertEqual(after_count, before_count+1)
