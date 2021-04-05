from django.contrib import messages
from django.contrib.auth import logout as dj_logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import \
    PasswordResetTokenGenerator as TokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from user.models import User

from .forms import LoginForm, RegisterForm

# Views

def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)

        # send activation mail
        send_activation_email(request,form.cleaned_data.get('email'), user)

        # save the user
        user.save()

        return redirect("login")
    return render(request, "authen/register.html", {"form":form})


def login (request):

    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        dj_login(request, form.user_cache)
        return redirect("user_profile")
    return render(request, "authen/login.html", {"form": form})


def logout(request):

    dj_logout(request)
    messages.info(request , "You have successfully logged out.")
    return redirect("login")



# Create token object 
activation_token = TokenGenerator()

def activate(request, uidb64, token):

    # Decode the token
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None 
    # Check if user is found and decoding is done
    if user and activation_token.check_token(user,token):
        # Activate the user
        user.is_active = True
        user.save()
        # TODO: Activation is done 
        return redirect ("login")

    # TODO: Activation link is invalid
    else:
        return redirect("login")
        


# Helpers

def send_activation_email(request, receiver_email, user):
    current_site = get_current_site(request)
    mail_subject = 'Account Activation'

    # Construct the email

    body = render_to_string('authen/email_activation.html',{

        'user':user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user),
    })

    email = EmailMessage(
        mail_subject, body, to=[receiver_email]
    )

    # send the email
    email.send()

