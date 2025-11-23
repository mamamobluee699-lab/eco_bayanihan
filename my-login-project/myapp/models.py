from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    zone = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"