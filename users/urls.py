from django.contrib.auth.views import (LoginView, LogoutView)
from django.urls import path

from users.views import register, add_contact, add_subscriber, ProfileUpdateView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='index'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('add_contact/', add_contact, name='add_contact'),
    path('add_subscriber/', add_subscriber, name='add_subscriber'),
    path('update/', ProfileUpdateView.as_view(), name='update'),
]
