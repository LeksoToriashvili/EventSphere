from django.urls import path

from events.views import (event_list,
                          event_detail,
                          event_create,
                          register_event,
                          user_dashboard)

urlpatterns = [
    path('', event_list, name='event_list'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('create/', event_create, name='event_create'),
    path('<int:event_id>/register/', register_event, name='register_event'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
]
