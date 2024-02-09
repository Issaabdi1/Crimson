from django import template
from tasks.models import Notification

register = template.Library()

@register.simple_tag
def get_notifications(user):
    """Returns a list of notifications for the given user"""
    return list(reversed(Notification.objects.filter(user = user)))

