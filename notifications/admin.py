from django.contrib import admin
from django.contrib.admin import register

from notifications.models import Notification


@register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'message', 'is_read', 'timestamp')
