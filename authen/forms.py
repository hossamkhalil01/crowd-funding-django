import logging

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from user.models import User

PHONE_REGEX = RegexValidator(r'^01[0-2][0-9]{8}$', 'Egyptian phone number is required')



class RegisterForm (forms.ModelForm):

    password1 = forms.CharField(
        label='Password', 
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        #help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone']


    # Validate the password
    def clean_password1(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # Validate the password
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)

        return password1

    # Validate the passwords matching
    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # Check if the passwords are identical
        if password1 != password2:
            self.add_error('password2', "Passwords don't match")
        return password2


    def save(self,commit=True):

        # Save the password in hashed format
        user = super(RegisterForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # wait for confirmation email
        user.is_active = False 
        
        if commit:
            user.save()
        return user


class LoginForm (AuthenticationForm):

    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

    error_messages = {

        'invalid_login':"Invalid Email or password.",

        'inactive':"Please confirm your email.",
    }
