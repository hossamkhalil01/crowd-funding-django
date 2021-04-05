from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Campaign, Donation


def donate(request,campaign_id):
    
    context = {"campaign": get_object_or_404(Campaign,pk=campaign_id)}
    
    if request.method == "POST":
        amount = request.POST.get('amount','invalid')

        # validate
        if amount and amount.isnumeric():
            Donation.objects.create(amount = amount, campaign_id=campaign_id, donator_id= request.user.id)
            messages.success(request, 'Your Donation Was Successfully Completed!')
            return redirect('campaign_show', campaign_id)

        else:
            messages.error(request, 'Invalid amount')


    return render(request, 'campaign/donation.html', context)
