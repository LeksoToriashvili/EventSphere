from itertools import count

from notifications.models import Notification


def notification_count(request):
    count = 0
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user).filter(is_read=False).count()
    return dict(notification_count=count)
