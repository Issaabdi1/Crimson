"""Tests for the upload_file view."""
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Upload, Team, SharedFiles
from tasks.forms import FileForm
from tasks.tests.helpers import reverse_with_next


class UploadFileViewTest(TestCase):
    """Test suite for the upload_file view."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        self.url = reverse('upload_file')
        mock_file = SimpleUploadedFile(f'test_upload_file_view_file.pdf', b'file_content')
        self.form_input = {
            'file': mock_file
        }

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()

    def test_upload_file_url(self):
        self.assertEqual(self.url, '/upload_file/')

    def test_get_upload_file(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_file.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, FileForm))

    def test_get_upload_file_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_file_upload(self):
        self.login(self.user)
        before_count = Upload.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Upload.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertTemplateUsed(response, 'upload_file.html')
        upload_file = Upload.objects.first()
        self.assertEqual(upload_file.file.name, f'user_@johndoe/test_upload_file_view_file.pdf')
        self.assertEqual(upload_file.owner, self.user)
        upload_file.delete()

    def test_unsuccessful_file_upload_with_wrong_file_extension(self):
        self.login(self.user)
        before_count = Upload.objects.count()
        self.form_input['file'] = SimpleUploadedFile(f'test_file.txt', b'file_content')
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Upload.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'upload_file.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, FileForm))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Only files with the extension .pdf are supported.')

    def test_unsuccessful_file_upload_with_amazon_s3_not_setup(self):
        settings.USE_S3 = False
        self.login(self.user)
        before_count = Upload.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Upload.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'upload_file.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, FileForm))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'The Amazon S3 service is not connected.')
        settings.USE_S3 = True

    def test_unsuccessful_file_upload_with_no_file(self):
        self.login(self.user)
        before_count = Upload.objects.count()
        self.form_input = {}
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Upload.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'upload_file.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, FileForm))

    def test_post_upload_file_to_a_team(self):
        self.login(self.user)
        team = Team.objects.create(name='Test Team upload')
        team.members.add(self.user)
        team.save()
        self.form_input['team_id'] = 1
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(team.shared_uploads.count(), 1)

    def test_post_upload_file_with_sharing_via_username(self):
        self.login(self.user)
        self.form_input['share'] = self.other_user.username
        before_count_upload = Upload.objects.count()
        before_count_shared = SharedFiles.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count_upload = Upload.objects.count()
        after_count_shared = SharedFiles.objects.count()
        self.assertEqual(after_count_upload, before_count_upload + 1)
        self.assertEqual(after_count_shared, before_count_shared + 1)
        self.assertTemplateUsed(response, 'upload_file.html')
        upload_file = Upload.objects.first()
        self.assertEqual(upload_file.file.name, f'user_@johndoe/test_upload_file_view_file.pdf')
        self.assertEqual(upload_file.owner, self.user)

    def test_post_upload_file_with_sharing_via_email(self):
        self.login(self.user)
        self.form_input['share'] = self.other_user.email
        before_count_upload = Upload.objects.count()
        before_count_shared = SharedFiles.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count_upload = Upload.objects.count()
        after_count_shared = SharedFiles.objects.count()
        self.assertEqual(after_count_upload, before_count_upload + 1)
        self.assertEqual(after_count_shared, before_count_shared + 1)
        self.assertTemplateUsed(response, 'upload_file.html')
        upload_file = Upload.objects.first()
        self.assertEqual(upload_file.file.name, f'user_@johndoe/test_upload_file_view_file.pdf')
        self.assertEqual(upload_file.owner, self.user)

    def test_post_upload_file_with_sharing_fail_with_wrong_input(self):
        self.login(self.user)
        self.form_input['share'] = 'xxxxxx'
        before_count_upload = Upload.objects.count()
        before_count_shared = SharedFiles.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count_upload = Upload.objects.count()
        after_count_shared = SharedFiles.objects.count()
        self.assertEqual(after_count_upload, before_count_upload + 1)
        self.assertEqual(after_count_shared, before_count_shared)
        self.assertTemplateUsed(response, 'upload_file.html')
        upload_file = Upload.objects.first()
        self.assertEqual(upload_file.file.name, f'user_@johndoe/test_upload_file_view_file.pdf')
        self.assertEqual(upload_file.owner, self.user)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'File has been uploaded but not shared. Provided username or email does not exist.')

    def test_post_upload_file_with_sharing_fail_with_no_input(self):
        self.login(self.user)
        self.form_input['share'] = ''
        before_count_upload = Upload.objects.count()
        before_count_shared = SharedFiles.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count_upload = Upload.objects.count()
        after_count_shared = SharedFiles.objects.count()
        self.assertEqual(after_count_upload, before_count_upload + 1)
        self.assertEqual(after_count_shared, before_count_shared)
        self.assertTemplateUsed(response, 'upload_file.html')
        upload_file = Upload.objects.first()
        self.assertEqual(upload_file.file.name, f'user_@johndoe/test_upload_file_view_file.pdf')
        self.assertEqual(upload_file.owner, self.user)


    def test_post_upload_file_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def login(self, user):
        self.client.login(username=user.username, password='Password123')