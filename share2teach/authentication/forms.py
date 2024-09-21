from django import forms
from django.contrib.auth.models import User
from .models import User, Educator, Moderator, Subject


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'subject_major', 'affiliation']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if self.instance.user_type not in ['Educator', 'Moderator']:
            self.fields.pop('subject_major', None)
            self.fields.pop('affiliation', None)


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    user_type = forms.ChoiceField(choices=[('educator', 'Educator'), ('moderator', 'Moderator')], label="User Type")  # Adjust choices as needed
    subject_major = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Major Subject")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'subject_major', 'affiliation']  # Include user_type here

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'subject_major', 'affiliation']

    def __init__(self, *args, **kwargs):
        super(AdminUserEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['user_type'].choices = [
                ('moderator', 'Moderator'),
                ('educator', 'Educator')
            ]
    def __init__(self, *args, **kwargs):
        super(AdminUserEditForm, self).__init__(*args, **kwargs)
        if self.instance.user_type not in ['educator', 'moderator']:
            self.fields.pop('subject_major', None)
            self.fields.pop('affiliation', None)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'subject_major', 'affiliation', 'is_email_verified']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }


