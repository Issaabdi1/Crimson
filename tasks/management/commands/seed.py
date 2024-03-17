from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from tasks.models import User, Upload, Team, ProfileImage, SharedFiles, Notification
import pytz
from faker import Faker
from random import randint, random
import os
import requests
import time
from django.utils import timezone

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    # Seeding User, Upload, Team associated with shared-file, ProfileImage, SharedFile associated with notifications
    # User seeding constants
    USER_COUNT = 20
    # Upload seeding constants
    UPLOAD_COUNT = 100
    UPLOAD_PER_USER = int(UPLOAD_COUNT / USER_COUNT)  # Remember to make it to be integer
    # Team seeding constants
    TEAM_COUNT = 30
    USER_PER_TEAM = 5
    UPLOAD_PER_TEAM = 2 * USER_PER_TEAM
    # Image seeding constants
    IMAGE_PER_USER = 2  # image_count = image_per_user * user_count
    # SharedFile seeding constants
    SHARED_FILE_PER_USER = 3  # shared_file_count = shared_file_per_user * user_count
    USER_PER_SHARED_FILE = 4

    DEFAULT_PASSWORD = 'Password123'
    pdf_url_prefix = 'https://mypdfbucket01.s3.eu-west-2.amazonaws.com/media/seeder_data/pdf/sample_file_'
    image_url_prefix = 'https://mypdfbucket01.s3.eu-west-2.amazonaws.com/media/seeder_data/image/image'
    help = 'Seeds the database with sample data'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        self.users = User.objects.all()
        self.uploads = Upload.objects.all()
        self.teams = Team.objects.all()
        self.images = ProfileImage.objects.all()
        self.shared_files = SharedFiles.objects.all()
        self.notifications = Notification.objects.all()

    def handle(self, *args, **options):
        self.create_users()
        self.users = User.objects.all()
        seed_upload_success = False
        if self.users.count() == self.USER_COUNT:
            self.create_uploads()
            self.uploads = Upload.objects.all()
            seed_upload_success = True
        else:
            print("Upload seeding terminated, since user seeding failed.      ")
        seed_image_success = False
        if seed_upload_success:
            self.create_images()
            self.images = ProfileImage.objects.all()
            seed_image_success = True
        else:
            print("Upload seeding terminated, since user seeding failed.      ")
        seed_team_success = False
        if seed_image_success:
            self.create_teams()
            self.teams = Team.objects.all()
            seed_team_success = True
        else:
            print("Team seeding terminated, since image seeding failed.    ")
        if seed_team_success:
            self.create_shared_files()
            self.shared_files = SharedFiles.objects.all()
            print("Seeding completed.      ")
        else:
            print("SharedFile seeding terminated, since team seeding failed.    ")

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def create_uploads(self):
        self.generate_random_uploads()

    def create_images(self):
        self.generate_random_images()

    def create_teams(self):
        self.generate_random_teams()

    def create_shared_files(self):
        self.generate_random_shared_files()

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
        start_time = time.time()
        upload_count = Upload.objects.count()
        if upload_count < self.UPLOAD_COUNT:
            for user in self.users:
                for i in range(0, int(Command.UPLOAD_PER_USER)):
                    print(f"Seeding upload {upload_count}/{self.UPLOAD_COUNT}", end='\r')
                    self.generate_upload(user)
                    upload_count = Upload.objects.count()
        end_time = time.time()
        print("Upload seeding complete.        ")
        print(f"Time taken: {int(end_time - start_time)} seconds.")

    def generate_random_images(self):
        start_time = time.time()
        image_count = ProfileImage.objects.count()
        if image_count < self.IMAGE_PER_USER * self.USER_COUNT:
            for user in self.users:
                for i in range(0, self.IMAGE_PER_USER):
                    print(f"Seeding image {image_count}/{self.IMAGE_PER_USER * self.USER_COUNT}", end='\r')
                    self.generate_image(user)
                    image_count = ProfileImage.objects.count()
        end_time = time.time()
        print("Image seeding complete.        ")
        print(f"Time taken: {int(end_time - start_time)} seconds.")

    def generate_random_teams(self):
        team_count = Team.objects.count()
        while team_count < self.TEAM_COUNT:
            print(f"Seeding team {team_count}/{self.TEAM_COUNT}", end='\r')
            users = []
            for i in range(0, self.USER_PER_TEAM):
                user = self.users[randint(0, self.USER_COUNT - 1)]
                while user in users:
                    user = self.users[randint(0, self.USER_COUNT - 1)]
                users.append(user)
            self.generate_team(users)
            team_count = Team.objects.count()
        print("Team seeding complete.      ")

    def generate_random_shared_files(self):
        shared_file_count = SharedFiles.objects.count()
        if shared_file_count < self.SHARED_FILE_PER_USER * self.USER_COUNT:
            for user in self.users:
                users_upload = Upload.objects.filter(owner=user)
                used_upload = []
                for i in range(0, self.SHARED_FILE_PER_USER):
                    print(f"Seeding shared file {shared_file_count}/{self.SHARED_FILE_PER_USER * self.USER_COUNT}",
                          end='\r')
                    upload = users_upload[randint(0, self.UPLOAD_PER_USER - 1)]
                    while upload in used_upload:
                        upload = users_upload[randint(0, self.UPLOAD_PER_USER - 1)]
                    self.generate_shared_file(user, upload)
                    used_upload.append(upload)
                    shared_file_count = SharedFiles.objects.count()
        print("SharedFile seeding complete.      ")

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})

    def generate_upload(self, user):
        owner = user
        comments = create_comment()
        url = create_pdf_url()
        self.try_create_upload({'owner': owner, 'comments': comments, 'url': url})

    def generate_image(self, user):
        user = user
        url = create_image_url()
        self.try_create_image({'user': user, 'url': url})

    def generate_team(self, users):
        name = create_team_name()
        users = users
        shared_uploads = self.create_team_shared_uploads(users)
        self.try_create_team({'users': users, 'name': name, 'shared_uploads': shared_uploads})

    def generate_shared_file(self, user, upload):
        shared_by = user
        shared_file = upload
        shared_to = self.create_shared_file_shared_to(user)
        self.try_create_shared_file({'shared_by': shared_by, 'shared_file': shared_file, 'shared_to': shared_to})

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

    def try_create_image(self, data):
        try:
            self.create_image(data)
        except:
            pass

    def try_create_team(self, data):
        try:
            self.create_team(data)
        except:
            pass

    def try_create_shared_file(self, data):
        try:
            self.create_shared_file(data)
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
        else:
            print('upload create unsuccessfully')
            return None

    def create_image(self, data):
        response = requests.get(data['url'])
        if response.status_code == 200:
            user = data['user']
            with open("temp.png", "wb") as f:
                f.write(response.content)

            image = ProfileImage.objects.create(
                user=user,
            )
            with open("temp.png", "rb") as f:
                image.image.save(os.path.basename(data['url']), File(f))
            os.remove("temp.png")
            user.avatar_url = image.image.url
            user.save()
        else:
            print('image create unsuccessfully')
            return None

    def create_team(self, data):
        team = Team.objects.create(
            name=data['name'],
        )
        for user in data['users']:
            team.members.add(user)
        for upload in data['shared_uploads']:
            team.shared_uploads.add(upload)
        team.save()

    def create_shared_file(self, data):
        shared_file = SharedFiles.objects.create(
            shared_file=data['shared_file'],
            shared_by=data['shared_by']
        )
        for user in data['shared_to']:
            shared_file.shared_to.add(user)
            Notification.objects.create(
                shared_file_instance=shared_file,
                user=user,
                time_of_notification=timezone.now(),
                notification_message=f'{data['shared_by'].username} shared a file with you'
            )
        shared_file.save()

    def create_team_shared_uploads(self, users):
        shared_uploads = []
        for user in users:
            users_upload = Upload.objects.filter(owner=user)
            for i in range(0, int(self.UPLOAD_PER_TEAM / self.USER_PER_TEAM)):
                upload = users_upload[randint(0, self.UPLOAD_PER_USER - 1)]
                while upload in shared_uploads:
                    upload = users_upload[randint(0, self.UPLOAD_PER_USER - 1)]
                shared_uploads.append(upload)
        return shared_uploads

    def create_shared_file_shared_to(self, user):
        shared_to = []
        for i in range(0, self.USER_PER_SHARED_FILE):
            user_shared_to = self.users[randint(0, self.USER_COUNT - 1)]
            while user_shared_to in shared_to or user_shared_to == user:
                user_shared_to = self.users[randint(0, self.USER_COUNT - 1)]
            shared_to.append(user_shared_to)
        return shared_to


def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()


def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'


def create_comment():
    fake = Faker()
    description = fake.paragraphs(3)
    return description


def create_pdf_url():
    return f'{Command.pdf_url_prefix}{str(randint(0, 10))}.pdf'


def create_image_url():
    return f'{Command.image_url_prefix}{str(randint(1, 21))}.png'


def create_team_name():
    fake = Faker()
    return f'Team {fake.word()}'
