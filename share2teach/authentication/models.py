from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('educator', 'Educator'),
        ('moderator', 'Moderator'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='educator')
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# Educator Model
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Educator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    subjects = models.ManyToManyField(Subject, related_name='educators')

    def __str__(self):
        return self.user.username
