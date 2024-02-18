"""Tests for the team detail view."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Upload, Team
from tasks.forms import AddUserToTeamForm
from tasks.tests.helpers import reverse_with_next


class TeamDetailViewTest(TestCase):
    """Test suite for the team detail view."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        self.invitee = User.objects.get(username='@petrapickles')

        self.team = Team.objects.create(name="test team")
        self.team.members.add(self.user)
        self.team.members.add(self.other_user)

        file_content = b'test file content'
        mock_file = SimpleUploadedFile(f'test_team_detail_view_file.pdf', file_content)
        self.upload = Upload.objects.create(owner=self.user, file=mock_file)
        self.team.shared_uploads.add(self.upload)

        self.url = reverse('team_detail', kwargs={'team_id': 1})
        self.form_input = {
            'username': "@petrapickles"
        }

    def tearDown(self):
        self.upload.delete()

    def test_team_detail_url(self):
        self.assertEqual(self.url, '/team_detail/1')

    def test_get_team_detail(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team_detail.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AddUserToTeamForm))
        self.assertEqual(response.context['team'], self.team)
        self.assertEqual(response.context['members'].count(), 2)
        self.assertEqual(response.context['shared_uploads'].count(), 1)

    def test_successful_user_invitation(self):
        self.login(self.user)
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'team_detail.html')
        self.assertTrue(self.invitee in self.team.members.all())
        self.assertEqual(response.context['team'], self.team)
        self.assertEqual(response.context['members'].count(), 3)
        self.assertEqual(response.context['shared_uploads'].count(), 1)

    def test_unsuccessful_user_invitation_with_wrong_username(self):
        self.login(self.user)
        self.form_input['username'] = '@user_not_exist'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'team_detail.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AddUserToTeamForm))
        self.assertEqual(response.context['team'], self.team)
        self.assertEqual(response.context['members'].count(), 2)
        self.assertEqual(response.context['shared_uploads'].count(), 1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'The user invited is not exist, please try another one.')

    def test_unsuccessful_user_invitation_with_empty_input(self):
        self.login(self.user)
        self.form_input = {}
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'team_detail.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AddUserToTeamForm))
        self.assertEqual(response.context['team'], self.team)
        self.assertEqual(response.context['members'].count(), 2)
        self.assertEqual(response.context['shared_uploads'].count(), 1)

    def test_get_team_detail_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_team_detail_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def login(self, user):
        self.client.login(username=user.username, password='Password123')