from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_organizer', 'is_attendee')
    list_filter = ('is_organizer', 'is_attendee')
