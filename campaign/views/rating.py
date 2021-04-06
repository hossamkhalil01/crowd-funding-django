from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Campaign, Rating


@login_required
def rate(request, campaign_id):

    if request.method == "POST":
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        context = {"campaign": campaign}

        rate = request.POST.get('rate', '')

        # validate
        if rate and rate.isnumeric():

            apply_rating(campaign, request.user, rate)

    return redirect('campaign_show', campaign_id)


def apply_rating(campaign, user, rate):

    prev_rating = campaign.ratings.filter(user_id=user.id)

    # has rated for this campaign before
    if prev_rating:

        prev_rating[0].value = int(rate)
        prev_rating[0].save()

    # first time
    else:
        Rating.objects.create(
            value=rate, campaign_id=campaign.id, user_id=user.id)
