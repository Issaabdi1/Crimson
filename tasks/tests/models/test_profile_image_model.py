"""Unit tests for the ProfileImage model."""
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from tasks.models import User, ProfileImage


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
        for image in self.images:
            if image:
                image.delete()

    def test_valid_profile_image(self):
        for image in self.images:
            self._assert_profile_image_is_valid(image)

    def test_profile_image_user_cannot_be_null(self):
        """Test that the user cannot be null."""
        image = ProfileImage(image=self.mock_images[0])
        self._assert_profile_image_is_invalid(image)

    def test_user_can_only_have_five_profile_images(self):
        image = ProfileImage.objects.create(user=self.user,
                                            image=SimpleUploadedFile(f'test_profile_image_model_image_6.png',
                                                                     b'test_image'))
        self.assertEqual(5, self.user.profileimage_set.all().count())
        image.delete()

    def _assert_profile_image_is_valid(self, image):
        try:
            image.full_clean()
        except ValidationError:
            self.fail('Test profile image should be valid')

    def _assert_profile_image_is_invalid(self, image):
        with self.assertRaises(ValidationError):
            image.full_clean()
