from django.core.management.base import BaseCommand
from tasks.models import User
from django.conf import settings


class Command(BaseCommand):
    """Build automation command to create a superuser."""
    DEFAULT_PASSWORD = 'Password123'
    help = 'Creates a superuser with the default username and password for debugging purposes.'

    def handle(self, *args, **options):
        if settings.DEBUG:
            try:
                User.objects.create_superuser('@admin', 'admin@example.com', Command.DEFAULT_PASSWORD)
                self.stdout.write(self.style.SUCCESS('Successfully created superuser.'))
                self.stdout.flush()
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error creating superuser: {e}'))
                self.stderr.flush()
        else:
            self.stderr.write(self.style.ERROR('Not in DEBUG mode. Test superuser not created.'))
            self.stderr.flush()
