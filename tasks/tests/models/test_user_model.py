"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User
import urllib.parse
from urllib.parse import quote


class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    GRAVATAR_URL = "https://www.gravatar.com/avatar/363c1b0cd64dadffb867236a00e62986"

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_must_start_with_at_symbol(self):
        self.user.username = 'johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphanumericals_after_at(self):
        self.user.username = '@john!doe'
        self._assert_user_is_invalid()

    def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
        self.user.username = '@jo'
        self._assert_user_is_invalid()

    def test_username_may_contain_numbers(self):
        self.user.username = '@j0hndoe2'
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.user.username = '@@johndoe'
        self._assert_user_is_invalid()


    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()


    def test_full_name_must_be_correct(self):
        full_name = self.user.full_name()
        self.assertEqual(full_name, "John Doe")


    def test_default_gravatar(self):
        actual_gravatar_url = self.user.gravatar()
        expected_gravatar_url = self._gravatar_url(size=120)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def test_custom_gravatar(self):
        actual_gravatar_url = self.user.gravatar(size=100)
        expected_gravatar_url = self._gravatar_url(size=100)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def test_mini_gravatar(self):
        actual_gravatar_url = self.user.mini_gravatar()
        expected_gravatar_url = self._gravatar_url(size=60)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def _gravatar_url(self, size):
        gravatar_url = f"{UserModelTestCase.GRAVATAR_URL}?size={size}&default=mp"
        return gravatar_url


    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_generate_ui_avatar_url_with_full_name(self):
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        expected_initials = 'JD'
        expected_url = self._generate_ui_avatar_expected_url(name=expected_initials)
        actual_url = self.user.generate_ui_avatar_url()
        self.assertEqual(actual_url, expected_url, "Avatar URL with full name does not match expected format.")

    def test_generate_ui_avatar_url_with_first_name_only(self):
        self.user.first_name = 'John'
        self.user.last_name = ''
        expected_initials = 'J'
        expected_url = self._generate_ui_avatar_expected_url(name=expected_initials)
        actual_url = self.user.generate_ui_avatar_url()
        self.assertEqual(actual_url, expected_url, "Avatar URL with first name only does not match expected format.")

    def test_generate_ui_avatar_url_with_last_name_only(self):
        self.user.first_name = ''
        self.user.last_name = 'Doe'
        expected_initials = 'D'
        expected_url = self._generate_ui_avatar_expected_url(name=expected_initials)
        actual_url = self.user.generate_ui_avatar_url()
        self.assertEqual(actual_url, expected_url, "Avatar URL with last name only does not match expected format.")

    def test_generate_ui_avatar_url_with_no_name(self):
        self.user.first_name = ''
        self.user.last_name = ''
        expected_initials = 'AD'
        expected_url = self._generate_ui_avatar_expected_url(name=expected_initials)
        actual_url = self.user.generate_ui_avatar_url()
        self.assertEqual(actual_url, expected_url, "Avatar URL with no name does not match expected format.")

    def _generate_ui_avatar_expected_url(self, name):
        base_url = "https://ui-avatars.com/api/"
        params = {
            'name': name,
            'size': '128',
            'background': 'random',
            'font-size': '0.5',
            'length': '2'
        }
        url_params = quote(urllib.parse.urlencode(params), safe='=&')
        return f"{base_url}?{url_params}"