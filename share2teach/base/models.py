from django.db import models
from authentication.models import User

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
    
class Subjects(models.Model):
    name = models.CharField(max_length=100)
    # Other fields here

    def __str__(self):
        return self.name

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Report(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Report for {self.document.title}"
        

class Message(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message for report on {self.report.document.title}"

#MOREMI - DOCUMENT REPORTING ENDS HERE
        return self.name

'''class Rating(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)'''

#for upload files begin
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
#for upload files end

'''class UploadedFile(models.Model): #for upload files
    file = models.FileField(upload_to='uploads/')  #for upload files
    uploaded_at = models.DateTimeField(auto_now_add=True)  #for upload files

    def __str__(self): #for upload files
        return self.file.name #for upload files'''




