from django.urls import path

from events.views import (EventListView,
                          event_detail,
                          event_create,
                          register_event,
                          user_dashboard,
                          EventDeleteView,
                          CancelEventView,
                          contact, toggle_like,
                          )

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('create/', event_create, name='event_create'),
    path('<int:pk>/cancel/', CancelEventView.as_view(), name='cancel_event'),
    path('<int:pk>/delete', EventDeleteView.as_view(), name='event_delete'),
    path('<int:event_id>/register/', register_event, name='register_event'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('contact/', contact, name='contact'),
    path('<int:event_id>/like/', toggle_like, name='toggle_like'),
]
