"""notification related view"""
from django.contrib.auth.decorators import login_required
from tasks.models import Notification
from django.http import JsonResponse
from django.forms.models import model_to_dict


@login_required
def process_notification_delete(request):
    """Processes a deletion of any notification"""
    notification_id = request.GET.get('notification_id')
    for_tests = request.GET.get('for_tests') #this is true if this view is being used for tests
    if not for_tests:  
        #When not testing, either delete all notifications, or a specific notification 
        if notification_id=="delete-all":
                #delete all the notifications of this user
                Notification.objects.filter(user = request.user).delete()
        elif notification_id != '':
            #delete the notification passed in
            Notification.objects.filter(id=int(notification_id)).delete()
        notifications = list(reversed(Notification.objects.filter(user = request.user)))
        notifications = list(map(model_to_dict, notifications))
    else:
         #If testing, don't do anything to the database, and just return an empty list
         #The purpose of this is to just show that this view is run 
         notifications = []
    #Return the data as a JsonResponse
    data = {'notifications': notifications}
    return JsonResponse(data)

@login_required
def set_notifications_as_read(request):
    """Sets all the notifications of the current user as read"""
    #get all notifications
    notifications = Notification.objects.filter(user = request.user)
    #set all to read
    for notification in notifications:
        notification.read = True
        notification.save()

    return JsonResponse({})

    