from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Campaign, Donation


@login_required
def donate(request,campaign_id):
    
    campaign = get_object_or_404(Campaign,pk=campaign_id)
    context = {"campaign":campaign}
    
    if request.method == "POST":
        amount = request.POST.get('amount','invalid')

        # validate
        if amount and amount.isnumeric():
            
            apply_user_donation(campaign,request.user,amount)

            # messages.success(request, 'Your Donation Was Successfully Completed!')
            return redirect('campaign_show', campaign_id)

        else:
            messages.error(request, 'Invalid amount')


    return render(request, 'campaign/donation.html', context)


def apply_user_donation(campaign, user, amount):

    prev_donations = campaign.donations.filter(donator_id=user.id)

    # has donated for this campaign before
    if prev_donations:

        prev_donations[0].amount += int(amount) 
        prev_donations[0].save()
    
    # first time
    else:
        Donation.objects.create(amount = amount, campaign_id=campaign.id, donator_id= user.id)
    
