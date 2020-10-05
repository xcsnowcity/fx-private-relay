from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from .utils import get_available_numbers


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    twilio_sid = models.CharField(max_length=34, unique=True, blank=False)
    initiating_proxy_number = models.CharField(max_length=20, blank=False)
    initiating_real_number = models.CharField(max_length=20, blank=True)
    initiating_participant_sid = models.CharField(max_length=34, blank=False)
    status = models.CharField(max_length=20, blank=False)
    expiration = models.DateTimeField(null=True)


    def make_session_for_user(
        user, num_minutes=settings.DEFAULT_PHONE_SESSION_MINUTES
    ):
        Session.delete_expired_sessions()
        available_numbers = get_available_numbers()

