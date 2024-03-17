"""Tests for the list team view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Upload, Team
from tasks.forms import CreateTeamForm
from tasks.tests.helpers import reverse_with_next


class ListTeamViewTest(TestCase):
    """Test suite for the list team view."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('team_list')
        self.form_input_create = {
            'create_group': 'True',
            'name': "test team"
        }
        self.form_input_join = {
            'join_group': 'True'
        }

    def test_list_team_url(self):
        self.assertEqual(self.url, '/team_list/')

    def test_get_list_team(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_team.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateTeamForm))
        self.assertEqual(response.context['team_joined'].count(), 0)

    def test_get_list_team_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_team_created(self):
        self.login(self.user)
        before_count = Team.objects.count()
        response = self.client.post(self.url, self.form_input_create, follow=True)
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertTemplateUsed(response, 'list_team.html')
        new_team = Team.objects.first()
        self.assertEqual(new_team.name, "test team")
        self.assertEqual(response.context['team_joined'].count(), 1)

    def test_successful_team_joined(self):
        self.login(self.user)
        group = Team.objects.create(name="team join")
        self.form_input_join['invitation_code'] = group.invitation_code
        before_count = self.user.team_set.count()
        response = self.client.post(self.url, self.form_input_join, follow=True)
        after_count = self.user.team_set.count()
        self.assertEqual(after_count, before_count+1)
        self.assertTrue(group in self.user.team_set.all())
        self.assertRedirects(response, self.url, status_code=302, target_status_code=200)

    def test_unsuccessful_team_joined_with_empty_form_input(self):
        self.login(self.user)
        group = Team.objects.create(name="team join")
        before_count = self.user.team_set.count()
        response = self.client.post(self.url, self.form_input_join, follow=True)
        after_count = self.user.team_set.count()
        self.assertEqual(after_count, before_count)
        self.assertFalse(group in self.user.team_set.all())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_team.html')

    def test_unsuccessful_team_create_with_empty_form_input(self):
        self.login(self.user)
        self.form_input_create = {'create_group': 'True',}
        before_count = Team.objects.count()
        response = self.client.post(self.url, self.form_input_create, follow=True)
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'list_team.html')
        form = response.context['create_form']
        self.assertTrue(isinstance(form, CreateTeamForm))
        self.assertEqual(response.context['team_joined'].count(), 0)

    def test_unsuccessful_post_team_list(self):
        self.login(self.user)
        before_count = Team.objects.count()
        response = self.client.post(self.url, {}, follow=True)
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'list_team.html')
        form = response.context['create_form']
        self.assertTrue(isinstance(form, CreateTeamForm))
        self.assertEqual(response.context['team_joined'].count(), 0)

    def test_post_list_team_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input_create)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def login(self, user):
        self.client.login(username=user.username, password='Password123')