from django.test import TestCase, RequestFactory
from tasks.models import User
from tasks.views import preferences_view

class PreferencesViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test_user', email='test@example.com', password='top_secret'
        )
        self.theme_preferences = ['dark-mode', 'default-mode']

    def test_get_request(self):
        request = self.factory.get('/preferences/')
        request.user = self.user
        self.user.theme_preference = 'dark-mode'
        self.user.save()
        response = preferences_view(request)
        self.assertEqual(response.status_code, 200)

    def test_post_request(self):
        request = self.factory.post('/preferences/', {'themeSelection': 'dark-mode'})
        request.user = self.user
        response = preferences_view(request)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.theme_preference, 'dark-mode')
