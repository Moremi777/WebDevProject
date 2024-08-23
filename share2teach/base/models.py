from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    ADMIN = 'admin'
    EDUCATOR = 'educator'
    MODERATOR = 'moderator'

    USER_TYPES = [
        (ADMIN, 'Admin'),
        (EDUCATOR, 'Educator'),
        (MODERATOR, 'Moderator'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default=EDUCATOR)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

class subject(models.Model):
    name = models.CharField(max_length=100)


class Document(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


