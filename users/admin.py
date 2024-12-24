from django.contrib import admin
from django.contrib.admin import register

from users.models import CustomUser, Subscribers, Contact


@register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_organizer', 'is_attendee')
    list_filter = ('is_organizer', 'is_attendee')


@register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('email',)


@register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
