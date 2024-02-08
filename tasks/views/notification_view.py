"""notification related view"""
from django.contrib.auth.decorators import login_required
from tasks.models import Notification
from django.http import JsonResponse
from django.forms.models import model_to_dict


@login_required
def process_notification_delete(request):
    """Processes a deletion of any notification"""
    notification_id = request.GET.get('notification_id')
    if notification_id=="delete-all":
            #delete all notifications of this user
            Notification.objects.filter(user = request.user).delete()
    elif notification_id is not None:
        #delete
        Notification.objects.filter(id=int(notification_id)).delete()
    notifications = list(reversed(Notification.objects.filter(user = request.user)))
    notifications = list(map(model_to_dict, notifications))
    data = {'notifications': notifications}
    return JsonResponse(data)
    """
    if request.method =="POST":
        #delete the relevant notifications
        data = request.POST['delete']
        if data=="delete-all":
            #delete all notifications of this user
            Notification.objects.filter(user = request.user).delete()
        else:
            #delete
            Notification.objects.filter(id=int(data)).delete()
    return redirect(request.META['HTTP_REFERER'])
    #don't return anything
    """