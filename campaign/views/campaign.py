import datetime

from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ..models import Campaign, CampaignImage, Donation, Rating


def show(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    images = campaign.images.all()
    average_rating = campaign.ratings.all().aggregate(Avg('value'))[
        'value__avg']

    # return user rating if signed in
    user_rating = 0

    if request.user.is_authenticated:
        user_rating = campaign.ratings.get(user_id=request.user.id).value

    if average_rating is None:
        average_rating = 0
    donations = campaign.donations.all().aggregate(Sum('amount'))[
        'amount__sum']
    if donations is None:
        donations = 0
    tags = campaign.tags.all()
    delta = timezone.now() - campaign.start_date

    context = {'campaign_info': campaign, 'images': images, 'rating': average_rating*20,
               'tags': tags, 'donations': donations, 'days': delta.days, 'rating_range': range(5, 0, -1),
               'user_rating': user_rating}

    return render(request, 'campaign/show.html', context)
