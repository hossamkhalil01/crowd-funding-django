from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserForm
from .models import User, UserProfile

# Create your views here.

@login_required
def home(request):
    return render(request, 'home/index.html')

def edit(request, user_id):
    if request.method == "GET":
        current_user = User.objects.get(id=user_id)
        form = UserForm(instance=current_user)
        return render(request, 'user/edit.html', {'current_user': current_user, 'form': form})
    else:
        current_user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user_id=user_id)
        print(request.POST)
        form = UserForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            profile.avatar = user.avatar
            profile.save()
            user.save()
            return redirect('user_profile')

def delete(request, user_id):
    current_user = get_object_or_404(User, id=user_id)
    current_user.delete()
    return redirect('logout')
