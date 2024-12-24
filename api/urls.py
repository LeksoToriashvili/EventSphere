from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()

router.register(r'events', views.EventViewSet, basename='events')
router.register(r'notifications', views.NotificationViewSet, basename='notifications')
router.register(r'register', views.UserRegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]
