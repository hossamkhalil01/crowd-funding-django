import datetime

from django.db.models import Avg, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ..models import Campaign, CampaignImage, Rating


def show(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    images = campaign.images.all()
    average_rating = campaign.ratings.all().aggregate(Avg('value'))['value__avg']
    if average_rating is None:
        average_rating = 0
    donations = campaign.donations.all().aggregate(Sum('amount'))['amount__sum']
    if donations is None:
        donations = 0
    tags = campaign.tags.all()
    delta = timezone.now()- campaign.start_date
    return render(request, 'campaign/show.html' , {'campaign_info' : campaign ,'images':images,'rating':average_rating*20 , 'tags':tags , 'donations':donations , 'days':delta.days})
