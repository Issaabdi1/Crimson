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
        self.url_comment_clear = reverse('clear_comment')
        self.url_comment_save = reverse('save_comment')
        self.url_comment_get = reverse('get_comments')
        self.url_comment_update = reverse('update_comment')
        self.url_comment_delete = reverse('delete_text_comment')
        self.url_comment_get_json = reverse('get_comments_json', kwargs={'upload_id': 1, 'mark_id': 1})

        self.url_comment_update_status = reverse('update_comment_status')
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
        response = self.client.post(self.url_comment_clear, follow=True)
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

    def test_get_comment_update(self):
        self.login(self.user)
        response = self.client.get(self.url_comment_update)
        self.assertEqual(response.status_code, 405)

    def test_post_comment_update(self):
        self.login(self.user)
        post_data = {
            'comment_id': 1,
            'text': "test comment update"
        }
        response = self.client.post(self.url_comment_update, data=post_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, "test comment update")
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["message"], "Comment updated successfully")

    def test_post_update_comment_comment_not_found(self):
        self.login(self.user)
        post_data = {
            'comment_id': 999,
            'text': "test comment update"
        }
        response = self.client.post(self.url_comment_update, data=post_data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content.decode(), {'success': False, 'message': 'Comment not found'})

    def test_get_comment_update_status(self):
        self.login(self.user)
        response = self.client.get(self.url_comment_update_status)
        self.assertEqual(response.status_code, 405)

    def test_update_comment_status_invalid_content_type(self):
        self.login(self.user)
        response = self.client.post(self.url_comment_update_status, content_type='text/plain')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content.decode(), {'error': 'Invalid content type'})

    def test_update_comment_status_post(self):
        self.login(self.user)
        post_data = {
            'comment_id': self.comment.id,
            'resolved': True
        }
        response = self.client.post(self.url_comment_update_status, data=post_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        updated_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(updated_comment.resolved, True)
        expected_response = {'success': True, 'message': 'Comment status updated successfully.'}
        self.assertJSONEqual(response.content.decode(), expected_response)

    def test_update_comment_status_invalid_json(self):
        self.login(self.user)
        post_data = 'invalid json'
        response = self.client.post(self.url_comment_update_status, data=post_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content.decode(), {'error': 'Invalid JSON or empty payload'})

    def test_update_comment_status_comment_not_found(self):
        self.login(self.user)
        post_data = {
            'comment_id': 999,
            'resolved': True
        }
        response = self.client.post(self.url_comment_update_status, data=post_data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content.decode(), {'error': 'Comment not found'})

    def test_get_comment_get_json(self):
        self.login(self.user)
        response = self.client.get(self.url_comment_get_json)
        self.assertEqual(response.status_code, 200)
        expected_response = "{" + f'"comments": ' + "[{" + f'"id": {self.comment.mark_id}, "text": "{self.comment.text}", "commenter_id": {self.comment.id}, "commenter": 1, "resolved": false' + "}]}"
        self.assertEqual(expected_response, response.content.decode())

    def test_post_comment_delete(self):
        self.login(self.user)
        post_data = {
            'id': 1,
        }
        before_count = Comment.objects.count()
        response = self.client.post(self.url_comment_delete, data=post_data, content_type='application/json')
        after_count = Comment.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(before_count-1, after_count)
        self.assertFalse(Comment.objects.filter(id=1).exists())
        expected_response = {'status': 'success', 'message': 'Comment deleted successfully'}
        self.assertJSONEqual(response.content.decode(), expected_response)

