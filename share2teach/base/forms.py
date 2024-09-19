from django import forms
from .models import Report
from .models import UploadedFile

class ReportForm(forms.ModelForm):
    submitted_by = forms.CharField(required=False, label='Your name or email (optional)')

    class Meta:
        model = Report
        fields = ['reason', 'submitted_by']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'reason': 'Reason for reporting',
        }


#for upload file begin
class FileUploadForm(forms.Form):
    file = forms.FileField()
    #for upload file end