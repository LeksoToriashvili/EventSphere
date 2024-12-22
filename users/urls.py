from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='index'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]