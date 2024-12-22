from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    is_organizer = models.BooleanField(default=False, verbose_name=_("Organizer"))
    is_attendee = models.BooleanField(default=True, verbose_name=_("Attendee"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))

    def __str__(self):
        return self.username
