"""Unit tests for the ProfileImage model."""
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from tasks.models import User, ProfileImage
from django.conf import settings


class ProfileImageModelTestCase(TestCase):
    """Unit tests for the ProfileImage model."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

        self.mock_images = []
        self.images = []

        for i in range(1, 6):
            mock_image = SimpleUploadedFile(f'test_profile_image_model_image_{i}.png', b'test_image')
            image = ProfileImage.objects.create(user=self.user, image=mock_image)
            self.mock_images.append(mock_image)
            self.images.append(image)

    def tearDown(self):
        if ProfileImage.objects.all().count() > 0:
            ProfileImage.objects.all().delete()

    def test_valid_profile_image(self):
        for image in self.images:
            self._assert_profile_image_is_valid(image)

    def test_profile_image_user_cannot_be_null(self):
        """Test that the user cannot be null."""
        image = ProfileImage(image=self.mock_images[0])
        self._assert_profile_image_is_invalid(image)

    def test_default_profile_image_is_valid(self):
        """Test that the default profile image is valid."""
        default_user = User.objects.get(username='@janedoe')
        self.assertEqual(default_user.avatar_url, settings.DEFAULT_IMAGE_URL)

    def test_user_can_only_have_five_profile_images(self):
        """Test the save method will override the oldest image if user holds more than 5 avatars."""
        image = ProfileImage.objects.create(user=self.user,
                                            image=SimpleUploadedFile(f'test_profile_image_model_image_6.png',
                                                                     b'test_image'))
        image.save()
        self.assertEqual(5, self.user.profileimage_set.count())
        self.assertEqual(5, ProfileImage.objects.count())
        image.delete()

    def test_uploaded_image_url(self):
        """Test the image's url of the ProfileImage model."""
        for image in self.images:
            self.assertEqual(
                image.image.url,
                f'https://mypdfbucket01.s3.amazonaws.com/media/{quote(image.image.name)}'
            )

    def test_uploaded_image_name(self):
        """Test the image's name of the ProfileImage model."""
        for i in range(0, 5):
            self.assertEqual(self.images[i].image.name, f'profile_image/user_@johndoe/{self.mock_images[i].name}')

    def test_profile_image_delete(self):
        """Test that the ProfileImage delete will delete the image in the server"""
        self.assertEqual(ProfileImage.objects.count(), 5)
        for image in self.images:
            image_url = image.image.url
            self.assertEqual(urlopen(image_url).getcode(), 200)
            image.delete()
            self.assertFalse(ProfileImage.objects.filter(pk=image.pk).exists())
            with self.assertRaises(HTTPError):
                self.assertEqual(urlopen(image_url).getcode(), 403)
        self.assertEqual(ProfileImage.objects.count(), 0)
        self.images.clear()

    def _assert_profile_image_is_valid(self, image):
        try:
            image.full_clean()
        except ValidationError:
            self.fail('Test profile image should be valid')

    def _assert_profile_image_is_invalid(self, image):
        with self.assertRaises(ValidationError):
            image.full_clean()
