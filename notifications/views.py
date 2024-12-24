from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView

from notifications.models import Notification


class NotificationView(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = 'notification.html'
    context_object_name = 'notification'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        if obj.recipient != self.request.user:
            raise PermissionDenied("You do not have permission to view this notification.")

        obj.is_read = True
        obj.save()

        return obj


class NotificationDeleteView(DeleteView):
    model = Notification
    context_object_name = 'notification'
    success_url = reverse_lazy('user_dashboard')

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.recipient != self.request.user:
            raise PermissionDenied("You do not have permission to delete this notification.")
        return obj
