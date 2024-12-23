from django.contrib import admin

from events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'date', 'address', 'canceled', 'is_upcoming')
    list_filter = ('date', 'organizer', 'canceled')
    search_fields = ('title', 'description', 'address')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'date', 'address', 'latitude', 'longitude', 'image', 'canceled')
        }),
        ('Organizer', {
            'fields': ('organizer',)
        }),
        ('Attendees', {
            'fields': ('attendees',)
        }),
    )
