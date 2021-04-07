from .models import User
from campaign.models import Campaign, Donation
from .forms import UserForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum

# Create your views here.

@login_required
def profile(request):
    current_user_campaigns = Campaign.objects.filter(creator_id=request.user.id)
    campaigns = []
    for current_user_campaign in current_user_campaigns:
        one_image = current_user_campaign.images.all()
        if one_image:
            one_image = one_image[0]
            campaigns.append({
            'id': int(current_user_campaign.id),
            'title': current_user_campaign.title,
            'details': current_user_campaign.details,
            'image': one_image.path.url
        })
    return render(request, 'profile/index.html', {'campaigns': campaigns, 'donations': False})

@login_required
def donations(request):
    current_user_donations = Donation.objects.filter(donator_id=request.user.id)
    campaigns = Campaign.objects.all()
    return render(request, 'profile/index.html', {'current_user_donations': current_user_donations,
    'campaigns':campaigns, 'donations': True})

@login_required
def edit(request):
    if request.method == "GET":
        current_user = request.user
        return render(request, 'user/edit.html', {'current_user': current_user})
    else:
        current_user = request.user
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
