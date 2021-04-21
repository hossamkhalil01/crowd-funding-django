from campaign.models import Campaign, Donation
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EditForm
from .models import User, UserProfile

# Create your views here.


@login_required
def profile(request):
    current_user_campaigns = Campaign.objects.filter(
        creator_id=request.user.id)
    return render(request, 'profile/base.html', {'campaigns': current_user_campaigns, 'donations': False})


@login_required
def donations(request):
    current_user_donations = Donation.objects.filter(
        donator_id=request.user.id)
    campaigns = Campaign.objects.all()
    return render(request, 'profile/base.html', {'current_user_donations': current_user_donations,
                                                 'campaigns': campaigns, 'donations': True})


@login_required
def edit(request):
    if request.method == "GET":
        current_user = request.user
        return render(request, 'user/edit.html', {'current_user': current_user})
    else:
        current_user = request.user
        profile = UserProfile.objects.get(user_id=current_user.id)
        form = EditForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            user = form.save()
            profile.avatar = user.avatar
            profile.save()
            return redirect('user_profile')
        return render(request, 'user/edit.html', {'current_user': current_user, 'form': form})


@login_required
def delete(request):
    request.user.delete()
    return redirect('logout')


@login_required
def check_password(request):
    if request.is_ajax and request.method == "POST":
        password = request.POST.get("pass")
        is_password_correct = request.user.check_password(password)
        return JsonResponse({"is_password_correct": is_password_correct})
