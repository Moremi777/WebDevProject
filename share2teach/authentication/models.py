from django.db import models
from django.contrib.auth.models import AbstractUser

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('educator', 'Educator'),
        ('moderator', 'Moderator'),
        ('administrator', 'Administrator'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='educator')
    subject_major = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    affiliation = models.CharField(max_length=100, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, related_name='moderators')

    def __str__(self):
        return self.user.username

class Educator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, related_name='educators')

    def __str__(self):
        return self.user.username



class UserFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploader = models.CharField(max_length=100)  # You can modify as per your needs

    def __str__(self):
        return f"{self.uploader} - {self.file.name}"
