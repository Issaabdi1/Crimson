"""notification related view"""
from django.contrib.auth.decorators import login_required
from tasks.models import Notification
from django.http import JsonResponse
from django.forms.models import model_to_dict


@login_required
def process_notification_delete(request):
    """Processes a deletion of any notification"""
    notification_id = request.GET.get('notification_id')
    #If the string passed in is delete-all, delete all notifications. 
    #Otherwise, use the string as an id for a specific notification to delete
    if notification_id=="delete-all":
        Notification.objects.filter(user = request.user).delete()
    elif notification_id is not None:
        Notification.objects.filter(id=int(notification_id)).delete()
    #Convert the notifications from a list of models to a dictionary so JSON can handle it
    notifications = list(reversed(Notification.objects.filter(user = request.user)))
    notifications = list(map(model_to_dict, notifications))
    data = {'notifications': notifications}
    return JsonResponse(data)