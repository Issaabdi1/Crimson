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
        self.upload.delete()

    def test_valid_upload(self):
        """Test that the team are valid."""
        self._assert_team_is_valid()

    def _assert_team_is_valid(self):
        try:
            self.team.full_clean()
        except ValidationError:
            self.fail('Test team should be valid')

    def _assert_team_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.team.full_clean()
