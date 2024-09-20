from django import forms
from .models import Report
from .models import UsersDemo

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

