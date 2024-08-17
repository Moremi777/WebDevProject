from django import forms

#for upload files
class FileUploadForm(forms.Form):
    file = forms.FileField()