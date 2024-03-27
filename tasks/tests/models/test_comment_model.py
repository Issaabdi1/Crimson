"""Unit tests for the Comment model."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from tasks.models import User, Comment, Upload
from django.core.exceptions import ValidationError


class CommentModelTestCase(TestCase):
    """Unit tests for the ProfileImage model."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        mock_file = SimpleUploadedFile('test_voice_comment_model_file.pdf', '')
        self.upload = Upload.objects.create(owner=self.user, file=mock_file)
        self.comment = Comment.objects.create(
            commenter=self.user,
            upload=self.upload,
            mark_id=1,
            text="test comment model"
        )

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()
        if Comment.objects.all():
            Comment.objects.all().delete()

    def test_valid_comment(self):
        self._assert_comment_is_valid(self.comment)

    def test_comment_user_cannot_be_null(self):
        """Test that the upload cannot be null."""
        comment = Comment(
            commenter=self.user,
            mark_id=1,
            text="test comment model"
        )
        self._assert_comment_is_invalid(comment)

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment),
                         f'File {self.comment.upload.file.name} is Comment by {self.comment.commenter} on {self.comment.date} with text: {self.comment.text} in mark id: {self.comment.mark_id}')

    def test_comment_with_no_date(self):
        self.assertEqual(self.comment.formatted_date(), "Date not set")

    def test_comment_formatted_date(self):
        self.comment.date = timezone.now()
        self.assertEqual(self.comment.formatted_date(), f"today {self.comment.date.strftime('%H:%M')}")

        self.comment.date = timezone.now() - timezone.timedelta(days=1)
        self.assertEqual(self.comment.formatted_date(), f"yesterday {self.comment.date.strftime('%H:%M')}")

        self.comment.date = timezone.now() - timezone.timedelta(days=5)
        self.assertEqual(self.comment.formatted_date(), "5 days ago")

        self.comment.date = timezone.now() - timezone.timedelta(days=40)
        self.assertEqual(self.comment.formatted_date(), "1 month ago")

        self.comment.date = timezone.now() - timezone.timedelta(days=70)
        self.assertEqual(self.comment.formatted_date(), "2 months ago")

        self.comment.date = timezone.now() - timezone.timedelta(days=100)
        self.assertEqual(self.comment.formatted_date(), "3 months ago")

    def _assert_comment_is_valid(self, comment):
        try:
            comment.full_clean()
        except ValidationError:
            self.fail('Test comment should be valid')

    def _assert_comment_is_invalid(self, comment):
        with self.assertRaises(ValidationError):
            comment.full_clean()
