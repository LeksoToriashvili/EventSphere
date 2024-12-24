from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    is_organizer = models.BooleanField(default=False, verbose_name=_("Organizer"))
    is_attendee = models.BooleanField(default=True, verbose_name=_("Attendee"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='img/profile_default.png')

    def __str__(self):
        return self.username


class Subscribers(models.Model):
    email = models.EmailField(unique=True, verbose_name=_("Email"))

    def __str__(self):
        return self.email


class Contact(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    email = models.EmailField(verbose_name=_("Email"))
    subject = models.CharField(verbose_name=_("Subject"), max_length=100)
    message = models.TextField(verbose_name=_("Message"))

    def __str__(self):
        return f"{self.name} - {self.subject}"
