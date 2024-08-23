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


class UploadedFile(models.Model): #for upload files
    file = models.FileField(upload_to='uploads/')  #for upload files
    uploaded_at = models.DateTimeField(auto_now_add=True)  #for upload files

    def __str__(self): #for upload files
        return self.file.name #for upload files


