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

    def __str__(self):
        return f"Report on {self.document.title} by {self.reported_by if self.reported_by else 'Anonymous'}"

class Contributor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

'''class Document(models.Model):
#MOREMI - DOCUMENT REPORTING
class Document(models.Model):
    # Assuming you have a Document model that users can report
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)'''
    # Other fields

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

'''class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title'''

class Message(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message for report on {self.report.document.title}"

#MOREMI - DOCUMENT REPORTING ENDS HERE
        return self.name


#for upload files begin
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    file = models.CharField(max_length=255)  
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploader = models.CharField(max_length=100)  # You can modify as per your needs
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Replace 1 with a valid default user ID or any other default value


    def __str__(self):
        return self.file.name
        
#for upload files end

'''class UploadedFile(models.Model): #for upload files
    file = models.FileField(upload_to='uploads/')  #for upload files
    uploaded_at = models.DateTimeField(auto_now_add=True)  #for upload files

    def __str__(self): #for upload files
        return self.file.name #for upload files'''




