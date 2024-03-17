"""Tests for the leave team view."""
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
        self.other_user = User.objects.get(username='@janedoe')
        self.team = Team.objects.create(name="test leave")
        self.team.members.add(self.user)
        self.team.members.add(self.other_user)
        self.team.save()
        self.url = reverse('team_leave', args=[self.team.id])

    def test_get_team_leave(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse('team_list'), status_code=302, target_status_code=200)

    def test_get_team_leave_redirect_when_not_loged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_success_leave_team(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse('team_list'), status_code=302, target_status_code=200)
        self.assertFalse(self.team.members.filter(username=self.user.username).exists())

    def test_leave_not_exist_team(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('team_leave', args=[self.team.id + 1]), follow=True)
        self.assertRedirects(response, reverse('team_list'), status_code=302, target_status_code=200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'You are not allowed to access this team')

    def test_delete_team_when_user_is_the_only_member(self):
        self.client.login(username=self.user.username, password='Password123')
        other_team = Team.objects.create(name="test delete only member")
        other_team.members.add(self.user)
        other_team.save()
        response = self.client.get(reverse('team_leave', args=[other_team.id]), follow=True)
        self.assertRedirects(response, reverse('team_list'), status_code=302, target_status_code=200)
        self.assertQuerysetEqual(Team.objects.filter(pk=other_team.pk), Team.objects.none())
