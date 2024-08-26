from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

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


class UploadedFile(models.Model): #for upload files
    file = models.FileField(upload_to='uploads/')  #for upload files
    uploaded_at = models.DateTimeField(auto_now_add=True)  #for upload files

    def __str__(self): #for upload files
        return self.file.name #for upload files


