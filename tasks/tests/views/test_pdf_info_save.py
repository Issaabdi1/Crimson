"""Unit tests for the mark saving"""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from tasks.models import Upload, PDFInfo, User
from django.urls import reverse


class SavePdfInfoTestCase(TestCase):

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.uploaded_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        self.upload = Upload.objects.create(file=self.uploaded_file, owner=self.user)
        self.url = reverse('save_pdf_marks')

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()

    def login(self, user):
        self.client.login(username=user.username, password='Password123')

    def test_save_pdf_info_post(self):
        self.login(self.user)
        post_data = {
            'listOfSpans': 'test_spans',
            'upload_id': self.upload.id,
            'mark_id': 1,
            'listOfComments': 'test_comments'
        }

        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PDFInfo.objects.filter(upload=self.upload).exists())
        pdf_info = PDFInfo.objects.get(upload=self.upload)
        self.assertEqual(pdf_info.listOfSpans, 'test_spans')
        self.assertEqual(pdf_info.mark_id, 1)
        self.assertEqual(pdf_info.listOfComments, 'test_comments')

    def test_save_pdf_info_post_with_existing_mark(self):
        self.login(self.user)
        mark = PDFInfo.objects.create(upload=self.upload, mark_id=1, listOfSpans='1', listOfComments='1')
        post_data = {
            'listOfSpans': 'test_spans',
            'upload_id': self.upload.id,
            'mark_id': 2,
            'listOfComments': 'test_comments'
        }

        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PDFInfo.objects.filter(upload=self.upload).exists())
        pdf_info = PDFInfo.objects.get(upload=self.upload)
        self.assertEqual(pdf_info.listOfSpans, 'test_spans')
        self.assertEqual(pdf_info.mark_id, 2)
        self.assertEqual(pdf_info.listOfComments, 'test_comments')
        mark.refresh_from_db()
        self.assertEqual(mark.mark_id,2)
        self.assertEqual(mark.listOfSpans, 'test_spans')
        self.assertEqual(mark.listOfComments, 'test_comments')

    def test_save_pdf_info_post_invalid_upload_id(self):
        self.login(self.user)
        post_data = {
            'listOfSpans': 'test_spans',
            'upload_id': 999,
            'mark_id': 1,
            'listOfComments': 'test_comments'
        }
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(PDFInfo.objects.filter(mark_id=1).exists())

    def test_save_pdf_info_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
