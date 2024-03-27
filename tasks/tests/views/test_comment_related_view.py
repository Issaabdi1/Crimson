"""Unit tests for the Comment related views"""
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from tasks.models import Upload, PDFInfo, User, Comment
from django.urls import reverse


class CommentViewTestCase(TestCase):
    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.uploaded_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        self.upload = Upload.objects.create(file=self.uploaded_file, owner=self.user)
        self.mark = PDFInfo.objects.create(upload=self.upload, mark_id=1, listOfSpans='test_comment_view',
                                           listOfComments='test_comment_view')
        self.url_comment_delete = reverse('clear_comment')
        self.url_comment_save = reverse('save_comment')
        self.url_comment_get = reverse('get_comments')
        self.comment = Comment.objects.create(upload=self.upload, commenter=self.user, mark_id=1,
                                              text='test_comment_view')

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()
        if Comment.objects.all():
            Comment.objects.all().delete()

    def login(self, user):
        self.client.login(username=user.username, password='Password123')

    def test_post_clear_comment(self):
        self.login(self.user)
        before_count = Comment.objects.count()
        response = self.client.post(self.url_comment_delete, follow=True)
        after_count = Comment.objects.count()
        self.assertEqual(before_count - 1, after_count)
        self.assertEqual(response.status_code, 204)

    def test_post_save_comment(self):
        self.login(self.user)
        post_data = {
            'mark_id': 2,
            'upload_id': self.upload.id,
            'text': 'Test comment'
        }
        before_count = Comment.objects.count()
        response = self.client.post(self.url_comment_save, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(mark_id=2, upload_id=self.upload.id, text='Test comment',
                                               commenter=self.user).exists())
        after_count = Comment.objects.count()
        self.assertEqual(before_count + 1, after_count)

    def test_get_save_comment(self):
        self.login(self.user)
        response = self.client.get(self.url_comment_save)
        self.assertFalse(response.json()["success"])
        self.assertEqual(response.json()["error"], "Only POST requests are allowed")

    def test_get_comments_get(self):
        self.login(self.user)
        get_data = {
            'upload_id': self.upload.id,
            'mark_id': 1
        }
        response = self.client.get(self.url_comment_get, get_data)
        self.assertEqual(response.status_code, 200)
        resolve = "false"
        if self.comment.resolved: resolve = "true"
        expected_response = f'[' + "{" + f'"commenter": "{self.user.username}", "avatar_url": "{settings.DEFAULT_IMAGE_URL}", "text": "{self.comment.text}", "comment_id": {self.comment.mark_id}, "date": "{self.comment.formatted_date()}", "resolved": {resolve}' + "}" + f']'
        list_of_comments = response.json()['comments']
        self.assertEqual(expected_response, list_of_comments)

    def test_get_comments_with_parameters(self):
        self.login(self.user)
        response = self.client.get(self.url_comment_get)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content.decode(), {'error': 'Upload ID or Mark ID not provided'})

    def test_get_comments_with_wrong_parameters(self):
        self.login(self.user)
        get_data = {
            'upload_id': 999,
            'mark_id': 999
        }
        response = self.client.get(self.url_comment_get, get_data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["error"], "No Upload matches the given query.")

    def test_post_comments_get(self):
        self.login(self.user)
        response = self.client.post(self.url_comment_get)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["error"], "Only GET requests are allowed")
