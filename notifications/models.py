from django.db import models

from users.models import CustomUser


class Notification(models.Model):
    NEW_EVENT = 'new_event'
    EVENT_CANCELLED = 'event_cancelled'
    EVENT_REGISTERED = 'event_registered'
    EVENT_REMINDER = 'event_reminder'

    NOTIFICATION_TYPES = [
        (NEW_EVENT, 'New Event'),
        (EVENT_CANCELLED, 'Event Cancelled'),
        (EVENT_REGISTERED, 'Event Registered'),
        (EVENT_REMINDER, 'Event Reminder'),
    ]

    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.get_notification_type_display()} - {self.recipient.username}'

    class Meta:
        ordering = ['-timestamp']
