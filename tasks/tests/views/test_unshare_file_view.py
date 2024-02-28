from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from tasks.models import User, Upload, SharedFiles
from tasks.tests.helpers import reverse_with_next

class UnshareFileViewTestCase(TestCase):

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.second_user = User.objects.get(username='@janedoe')
        self.form_input = {
            'file-id': 1,
            'user-id': 2
        }
        self.test_file = SimpleUploadedFile(
            'test_file.pdf',
            b'Test file content',
            content_type='text/plain'
        )
        self.upload = Upload.objects.create(
            file=self.test_file,
            owner=self.user,
        )
        self.share = SharedFiles.objects.create(
            shared_file=self.upload,
            shared_by=self.user,
        )
        self.share.shared_to.add(self.second_user)
        self.url = reverse('unshare_file', args=[self.upload.id, self.second_user.id])

    def tearDown(self):
        self.upload.delete()


    def test_unshare_file_url(self):
        self.assertEqual(self.url,'/unshare_file/1/2/')

    def test_get_request_always_redirects(self):
        # Not logged in
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

        # Logged in
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        response_url = reverse('filelist')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'filelist.html')
        self.assertTemplateUsed(response, 'unshare_file.html')
    
    def test_successful_unshare_file(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = self.share.shared_to.count()
        response = self.client.post(self.url)
        after_count = self.share.shared_to.count()
        self.assertEqual(after_count, before_count - 1)
        response_url = reverse('filelist')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)