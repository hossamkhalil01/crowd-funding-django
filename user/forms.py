from django.forms import ModelForm
from user.models import User
from django import forms

class UserForm(ModelForm):
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar', 'birthdate', 'country', 'fb_account')