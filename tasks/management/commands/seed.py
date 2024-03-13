from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from tasks.models import User, Upload
import pytz
from faker import Faker
from random import randint, random
import os
import requests

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 20
    TEAM_COUNT = 5
    UPLOAD_COUNT = 100
    IMAGE_COUNT = 600
    UPLOAD_PER_USER = UPLOAD_COUNT / USER_COUNT
    DEFAULT_PASSWORD = 'Password123'
    pdf_url_prefix = 'https://mypdfbucket01.s3.eu-west-2.amazonaws.com/media/seeder_data/pdf/sample_file_'
    help = 'Seeds the database with sample data'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        self.users = User.objects.all()
        self.uploads = Upload.objects.all()

    def handle(self, *args, **options):
        self.create_users()
        self.users = User.objects.all()
        if self.users.count() == self.USER_COUNT:
            self.create_uploads()
            self.uploads = Upload.objects.all()
        else:
            print("User seeding failed.      ")

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def create_uploads(self):
        self.generate_random_uploads()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        user_count = User.objects.count()
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_random_uploads(self):
        upload_count = Upload.objects.count()
        while upload_count < self.UPLOAD_COUNT:
            for user in self.users:
                for i in range(0, int(Command.UPLOAD_PER_USER)):
                    print(f"Seeding upload {upload_count}/{self.UPLOAD_COUNT}", end='\r')
                    self.generate_upload(user)
                    upload_count = Upload.objects.count()
        print("Upload seeding complete.      ")

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})

    def generate_upload(self, user):
        owner = user
        comments = create_comment()
        url = create_url()
        self.try_create_upload({'owner': owner, 'comments': comments, 'url': url})

    def try_create_user(self, data):
        try:
            self.create_user(data)
        except:
            pass

    def try_create_upload(self, data):
        try:
            self.create_upload(data)
        except:
            pass

    def create_user(self, data):
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )

    def create_upload(self, data):
        response = requests.get(data['url'])
        if response.status_code == 200:
            with open("temp.pdf", "wb") as f:
                f.write(response.content)

            upload = Upload.objects.create(
                owner=data['owner'],
                comments=data['comments'],
            )

            # Open the temporary file and save it as the file field of the Upload object
            with open("temp.pdf", "rb") as f:
                upload.file.save(os.path.basename(data['url']), File(f))
            # Delete the temporary file
            os.remove("temp.pdf")
            return upload
        else:
            print('upload create unsuccessfully')
            return None


def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()


def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'


def create_comment():
    fake = Faker()
    description = fake.paragraphs(3)
    return description


def create_url():
    return f'{Command.pdf_url_prefix}{str(randint(0, 10))}.pdf'
