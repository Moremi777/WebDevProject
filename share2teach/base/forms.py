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
from .models import UploadedFile

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


            'reason': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'reason': 'Reason for reporting',
        }


#for upload file begin
class FileUploadForm(forms.Form):
    file = forms.FileField()
    #for upload file end


#the following code is for the drop box containing all subjects
SUBJECTS = [
    ('maths', 'Maths'),
    ('life_science', 'Life Science'),
    ('history', 'History'),
    ('english', 'English'),
    ('geography', 'Geography'),
    ('natural_science', 'Natural Science'),
    ('afrikaans', 'Afrikaans'),
    ('life_orientation', 'Life Orientation')
]

class SubjectForm(forms.Form):
    user_id = forms.IntegerField(label="User ID")
    subject = forms.ChoiceField(choices=SUBJECTS)

    def filter_subjects(self, user_id):
        try:
            user = UsersDemo.objects.get(user_id=user_id)
            # Set the available subject options based on user's subject
            self.fields['subject'].choices = [(user.subject, user.get_subject_display())]
        except UsersDemo.DoesNotExist:
            self.fields['subject'].choices = SUBJECTS  # If user doesn't exist, show all subjects

#the code ends here__________________________________________________________________________________

