from django.urls import path

from notifications.views import NotificationView, NotificationDeleteView

urlpatterns = [
    path('<int:pk>/', NotificationView.as_view(), name='notification_detail'),
    path('<int:pk>/delete/', NotificationDeleteView.as_view(), name='notification_delete'),
]
