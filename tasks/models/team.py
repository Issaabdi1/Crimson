from django.db import models
from . import User, Upload
import uuid


class Team(models.Model):
    """Model used for teams. A team can have many users, and many uploads."""
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(User)
    shared_uploads = models.ManyToManyField(Upload)
    invitation_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def add_upload(self, upload):
        self.shared_uploads.add(upload)