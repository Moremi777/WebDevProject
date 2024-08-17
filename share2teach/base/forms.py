from django import forms
<<<<<<< HEAD

#for upload files
class FileUploadForm(forms.Form):
    file = forms.FileField()
=======
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    affiliation = forms.CharField(max_length=255, required=False)
    phone = forms.CharField(max_length=255, required=True)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'affiliation', 'user_type')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data
>>>>>>> fd96fa894f51faa6a89861552f97c3c68ac90a1d
