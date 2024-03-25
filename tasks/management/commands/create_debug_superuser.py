import os
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from tasks.models import User, Upload
from django.conf import settings


class Command(BaseCommand):
    """Build automation command to create a superuser."""
    DEFAULT_PASSWORD = 'Password123'
    help = 'Creates a superuser with the default username and password for debugging purposes.'

    def handle(self, *args, **options):
        if settings.DEBUG:
            try:
                admin = User.objects.create_superuser('@admin', 'admin@example.com', Command.DEFAULT_PASSWORD)
                self.create_test_upload('https://mypdfbucket01.s3.eu-west-2.amazonaws.com/media/test_file/test_file_1.pdf',admin)
                self.create_test_upload('https://mypdfbucket01.s3.eu-west-2.amazonaws.com/media/test_file/test_file_2.pdf', admin)
                self.stdout.write(self.style.SUCCESS('Successfully created superuser.'))
                self.stdout.flush()
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error creating superuser: {e}'))
                self.stderr.flush()
        else:
            self.stderr.write(self.style.ERROR('Not in DEBUG mode. Test superuser not created.'))
            self.stderr.flush()

    def create_test_upload(self, url, user):
        response = requests.get(url)
        if response.status_code == 200:
            with open("temp.pdf", "wb") as f:
                f.write(response.content)
            upload = Upload.objects.create(
                owner=user,
                comments='',
            )
            with open("temp.pdf", "rb") as f:
                upload.file.save(os.path.basename(url), File(f))
            os.remove("temp.pdf")
        else:
            print('test upload for admin create unsuccessfully')
            return None