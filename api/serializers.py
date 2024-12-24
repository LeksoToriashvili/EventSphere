from rest_framework import serializers

from events.models import Event
from notifications.models import Notification
from users.models import CustomUser


class EventSerializer(serializers.ModelSerializer):
    attendees_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id']

    def get_attendees_count(self, obj):
        return obj.attendees.count()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_organizer', 'is_attendee', 'password', 'image')
