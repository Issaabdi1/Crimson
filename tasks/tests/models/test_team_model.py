"""Unit tests for the Team model."""
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from tasks.models import User, Team, Upload

class TeamModelTestCase(TestCase):
    """Unit tests for the Team model."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user1 = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        self.user3 = User.objects.get(username='@petrapickles')
        self.team = Team.objects.create(name='Test Team')

        for user in [self.user1, self.user2, self.user3]:
            self.team.members.add(user)

        file_content = b'test file content'
        mock_file = SimpleUploadedFile(f'test_team_model_file.pdf', file_content)
        self.upload = Upload.objects.create(owner=self.user1, file=mock_file)
        self.team.shared_uploads.add(self.upload)

    def tearDown(self):
        if Upload.objects.all():
            Upload.objects.all().delete()

    def test_valid_upload(self):
        """Test that the team are valid."""
        self._assert_team_is_valid()

    def test_team_shared_uploads(self):
        """Test that the team shared uploads are valid."""
        file_content = b'test file content'
        mock_file = SimpleUploadedFile(f'test_team_model_shared_file.pdf', file_content)
        dummy_upload = Upload.objects.create(owner=self.user1, file=mock_file)
        before_count = self.team.shared_uploads.count()
        self.team.add_upload(dummy_upload)
        self._assert_team_is_valid()
        after_count = self.team.shared_uploads.count()
        self.assertEqual(before_count + 1, after_count)

    def test_team_without_members_must_be_deleted(self):
        """Test that the team without members must be deleted."""
        team = Team.objects.create(name='Test Team')
        team.members.add(self.user1)
        self.user1.delete()
        self.assertQuerysetEqual(Team.objects.filter(pk=team.pk), Team.objects.none())

    def test_team_with_members_must_not_be_deleted(self):
        """Test that the team with members must not be deleted."""
        self.user1.delete()
        self.assertIsNotNone(Team.objects.filter(pk=self.team.pk).first())

    def _assert_team_is_valid(self):
        try:
            self.team.full_clean()
        except ValidationError:
            self.fail('Test team should be valid')

    def _assert_team_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.team.full_clean()
