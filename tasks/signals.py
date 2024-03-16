from django.db.models.signals import post_delete, m2m_changed
from django.dispatch import receiver
from .models import Upload, ProfileImage, Team, User


@receiver(post_delete, sender=Upload)
def remove_file_from_s3(sender, instance, **kwargs):
    instance.file.delete(save=False)


@receiver(post_delete, sender=ProfileImage)
def remove_file_from_s3(sender, instance, **kwargs):
    instance.image.delete(save=False)


@receiver(post_delete, sender=User)
def delete_team_with_deleted_user(sender, instance, **kwargs):
    """
    If a deleted user was the last member of a team, the team is deleted.
    """
    for team in Team.objects.all():
        if team.members.count() == 0:
            team.delete()