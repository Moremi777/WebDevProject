from django import forms
from .models import Subject
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

#for upload file begin
class FileUploadForm(forms.Form):
    file = forms.FileField()
    #for upload file end