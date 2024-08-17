from django.db import models

#THE FAQ MODEL
class FAQ(models.Model):
    STATUS_CHOICES = [
        ('published', 'Published'),
        ('draft', 'Draft'),
        ('archived', 'Archived'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('logged_in', 'Logged In Users'),
        ('admin_only', 'Admin Only'),
    ]

    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=255, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)  # You might use a ManyToMany field for tags in a more complex setup
    priority = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    author = models.CharField(max_length=255, blank=True, null=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')

    def __str__(self):
        return self.question