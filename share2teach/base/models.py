from django.db import models
from authentication.models import User

class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='documents/')
    avg_rating = models.FloatField(default=0.0)  # Store the average rating
    total_ratings = models.PositiveIntegerField(default=0)  # Total number of ratings
    ratings_sum = models.PositiveIntegerField(default=0)  # Sum of all ratings

    def calculate_average_rating(self):
        if self.total_ratings > 0:
            return self.ratings_sum / self.total_ratings
        return 0


class Rating(models.Model):
    session_id = models.CharField(max_length=255)
    document = models.ForeignKey(Document, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField() 

class Report(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    reported_by = models.EmailField(null=True, blank=True)  # Email field for open access users
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Report on {self.document.title} by {self.reported_by if self.reported_by else 'Anonymous'}"


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name


#