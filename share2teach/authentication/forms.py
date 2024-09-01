from django import forms
# forms.py

from django import forms
from django.contrib.auth.models import User

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }
