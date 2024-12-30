from http.client import responses

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response

from api.serializers import EventSerializer, NotificationSerializer, UserSerializer
from events.models import Event
from notifications.models import Notification
from users.models import CustomUser
from notifications.tasks import send_notification


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.author == request.user


class QuestionsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get', 'post']
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        event = self.get_object()

        if event.author != request.user:
            return Response(
                {'detail': 'Not authorized to cancel this event.'},
                status=status.HTTP_403_FORBIDDEN
            )

        event.canceled = True
        event.save()
        send_notification.delay(Notification.EVENT_CANCELLED, event.id)

        return Response(
            {'detail': 'Event canceled successfully.'},
            status=status.HTTP_200_OK
        )


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    http_method_names = ['get', 'delete', 'post']

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        return Response(
            {'detail': 'POST method is not allowed to create notifications here.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=True, methods=['post'])
    def set_read(self, request, pk=None):
        try:
            notification = self.get_object()

            if notification.recipient != request.user:
                return Response({'detail': 'Not authorized to update this notification.'},
                                status=status.HTTP_403_FORBIDDEN)

            notification.is_read = True
            notification.save()

            return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'detail': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']
