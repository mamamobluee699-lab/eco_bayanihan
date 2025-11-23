from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password


class CleanupEvent(models.Model):
    PLACE_CHOICES = [
        ('beach', 'Beach'),
        ('park', 'Park'),
        ('street', 'Street'),
        ('river', 'River'),
        ('general', 'General Cleanup'),
    ]

    name = models.CharField(max_length=200)
    place = models.CharField(max_length=20, choices=PLACE_CHOICES)
    specific_location = models.CharField(max_length=300, help_text='Specific address or location details')
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField(help_text='Duration in hours')
    points = models.IntegerField(default=10)
    max_participants = models.IntegerField(default=20)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"{self.name} ({self.date})"

class Participant(models.Model):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    birthdate = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(CleanupEvent, on_delete=models.CASCADE, related_name='participants', null=True,
    blank=True)  # ✅ allow blank in forms

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.fullname} ({self.username})"

    class Meta:
        ordering = ['-registered_at']




class CleanupRegistration(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(CleanupEvent, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    points_awarded = models.BooleanField(default=False)
    proof_image = models.ImageField(upload_to='proofs/', null=True, blank=True)
    proof_notes = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='approved_registrations'
    )

    class Meta:
        ordering = ['-registered_at']
        unique_together = (('participant', 'event'),)

    def __str__(self):
        return f"{self.participant.fullname} -> {self.event.name}"


class Activity(models.Model):
    CLEANUP_TYPES = CleanupEvent.PLACE_CHOICES
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(CleanupEvent, on_delete=models.CASCADE, null=True, blank=True)
    cleanup_type = models.CharField(max_length=20, choices=CLEANUP_TYPES, default='general')
    points_earned = models.IntegerField(default=10)
    date_participated = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.participant.fullname} +{self.points_earned} pts"

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class LoginAttempt(models.Model):
    username = models.CharField(max_length=150)
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    def is_locked(self):
        # Locked for 10 minutes after 5 failed attempts
        if self.attempts >= 5:
            if timezone.now() < self.last_attempt + timedelta(minutes=10):
                return True
            else:
                self.attempts = 0
                self.save()
                return False
        return False
