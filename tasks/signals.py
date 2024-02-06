from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Upload


@receiver(post_delete, sender=Upload)
def remove_file_from_s3(sender, instance, **kwargs):
    instance.file.delete(save=False)