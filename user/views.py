from .models import User
from .forms import UserForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

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
        print(request.POST)
        form = UserForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('user_profile')

def delete(request, user_id):
    current_user = get_object_or_404(User, id=user_id)
    current_user.delete()
    return redirect('logout')
