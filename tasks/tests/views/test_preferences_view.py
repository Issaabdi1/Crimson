from django.test import TestCase, RequestFactory
from tasks.models import User
from tasks.tests.helpers import reverse_with_next
from tasks.views import preferences_view


class PreferencesViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test_user', email='test@example.com', password='top_secret'
        )
        self.theme_preferences = ['dark-mode', 'default-mode']

    def test_get_request(self):
        self.client.login(username='test_user', password='top_secret')
        request = self.factory.get('/preferences/')
        request.user = self.user
        self.user.theme_preference = 'dark-mode'
        self.user.save()
        response = preferences_view(request)
        self.assertEqual(response.status_code, 200)

    def test_get_preference_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', '/preferences/')
        response = self.client.get('/preferences/')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_request(self):
        self.client.login(username='test_user', password='top_secret')
        request = self.factory.post('/preferences/', {'themeSelection': 'dark-mode'})
        request.user = self.user
        response = preferences_view(request)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.theme_preference, 'dark-mode')

    def test_unsuccessful_post_request(self):
        self.client.login(username='test_user', password='top_secret')
        request = self.factory.post('/preferences/', {'themeSelection': ''})
        request.user = self.user
        response = preferences_view(request)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.theme_preference, 'default-mode')

    def test_post_preference_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', '/preferences/')
        response = self.client.post('/preferences/', {'themeSelection': 'dark-mode'})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
