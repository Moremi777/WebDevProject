from django import forms
from .models import Report
from .models import Rating
from .models import Document

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
        

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reported_by', 'reason']  # Include 'reported_by' for the email field
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
            'reported_by': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),  # Email input field
        }

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file'] 

