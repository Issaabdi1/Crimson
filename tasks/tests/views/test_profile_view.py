"""Tests for the profile view."""
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from tasks.forms import UserForm, UploadProfileImageForm, AvatarForm
from tasks.models import User, ProfileImage
from tasks.tests.helpers import reverse_with_next, create_test_image
from django.conf import settings


class ProfileViewTest(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]



    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('profile')
        mock_image_to_upload = SimpleUploadedFile(
            'test_profile_view_upload_image.png',
            create_test_image().read(),
            content_type='image/png'
        )
        mock_image_for_model = SimpleUploadedFile(
            f'test_profile_view_profile_image_model.png',
            create_test_image().read(),
            content_type='image/png'
        )
        self.profile_image = ProfileImage.objects.create(image=mock_image_for_model, user=self.user)
        self.form_input_update = {
            'update_profile': 'True',
            'first_name': 'John2',
            'last_name': 'Doe2',
            'username': '@johndoe2',
            'email': 'johndoe2@example.org',
        }
        self.form_input_upload = {
            'image':  mock_image_to_upload,
            'upload_image':  'True',
        }
        self.form_input_avatar = {
            'update_avatar':  'True',
            'avatar_url': self.profile_image.image.url,
        }

    def tearDown(self):
        if ProfileImage.objects.all().count() > 0:
            ProfileImage.objects.all().delete()

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertEqual(form.instance, self.user)

    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccesful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input_update['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input_update)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')

    def test_unsuccessful_profile_update_due_to_duplicate_username(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input_update['username'] = '@janedoe'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input_update)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['profile_form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')

    def test_succesful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input_update, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@johndoe2')
        self.assertEqual(self.user.first_name, 'John2')
        self.assertEqual(self.user.last_name, 'Doe2')
        self.assertEqual(self.user.email, 'johndoe2@example.org')

    def test_successful_avatar_update(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input_avatar, follow=True)
        self.user.refresh_from_db()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(self.user.avatar_url, self.profile_image.image.url)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertEqual(str(messages_list[0]), f'Avatar updated successfully!')

    def test_unsuccessful_avatar_update(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input_avatar['avatar_url'] = 'BAD_URL'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input_avatar, follow=True)
        self.user.refresh_from_db()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(self.user.avatar_url, settings.DEFAULT_IMAGE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['avatar_form']
        self.assertTrue(isinstance(form, AvatarForm))
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertEqual(messages_list[0].message, 'Avatar update unsuccessfully.')

    def test_successful_image_upload(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = ProfileImage.objects.count()
        response = self.client.post(self.url, self.form_input_upload, follow=True)
        self.user.refresh_from_db()
        after_count = ProfileImage.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['upload_form']
        self.assertTrue(isinstance(form, UploadProfileImageForm))
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertEqual(str(messages_list[0]), f'Image uploaded successfully!')
        upload_image = ProfileImage.objects.all()[1]
        self.assertEqual(self.user.avatar_url, upload_image.image.url)
        self.assertEqual(upload_image.image.name, f'profile_image/user_@johndoe/test_profile_view_upload_image.png')
        self.assertEqual(upload_image.user, self.user)

    def test_unsuccessful_file_upload_with_wrong_file_extension(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = ProfileImage.objects.count()
        self.form_input_upload['image'] = SimpleUploadedFile(f'test_file.txt', b'file_content')
        response = self.client.post(self.url, self.form_input_upload, follow=True)
        self.user.refresh_from_db()
        after_count = ProfileImage.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['upload_form']
        self.assertTrue(isinstance(form, UploadProfileImageForm))
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertEqual(str(messages_list[0]), f'Image upload unsuccessfully.')

    def test_unsuccessful_image_upload_with_amazon_s3_not_setup(self):
        settings.USE_S3 = False
        self.client.login(username=self.user.username, password='Password123')
        before_count = ProfileImage.objects.count()
        response = self.client.post(self.url, self.form_input_upload, follow=True)
        self.user.refresh_from_db()
        after_count = ProfileImage.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['upload_form']
        self.assertTrue(isinstance(form, UploadProfileImageForm))
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertEqual(str(messages_list[0]), f'The Amazon S3 service is not connected.')
        settings.USE_S3 = True

    def test_unsuccessful_file_upload_with_no_file(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = ProfileImage.objects.count()
        self.form_input_upload = {}
        response = self.client.post(self.url, self.form_input_upload, follow=True)
        self.user.refresh_from_db()
        after_count = ProfileImage.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['upload_form']
        self.assertTrue(isinstance(form, UploadProfileImageForm))

    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input_update)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
