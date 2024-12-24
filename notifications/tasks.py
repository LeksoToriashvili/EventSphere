from celery import shared_task

from events.models import Event
from notifications.models import Notification


@shared_task
def send_notification(notification, event_id):
    event = Event.objects.get(id=event_id)
    attendees = event.attendees.all()

    for attendee in attendees:
        notification = Notification.objects.create(recipient=attendee, notification_type=notification,
                                                   message=f"something changed about event: {event.title}")
