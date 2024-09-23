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
from .models import UsersDemo
'''from .models import UploadedFile'''

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

        def clean_file(self):
            file = self.cleaned_data.get('file')
            if file:
                # File size check
                if file.size > 10 * 1024 * 1024:  # 10 MB
                    raise ValidationError("File size exceeds the limit of 10MB.")
                # File type check
                valid_extensions = ['.pdf', '.docx', '.xlsx', '.zip']
                if not any(file.name.endswith(ext) for ext in valid_extensions):
                    raise ValidationError("Invalid file type. Please upload a PDF, DOCX, XLSX, or ZIP file.")
            return file

