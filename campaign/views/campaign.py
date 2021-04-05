from django.contrib import messages
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Campaign, CampaignImage, Donation, Rating


def show(request, campaign_id):
    context = {"campaign": get_object_or_404(Campaign,pk=campaign_id)}
    return render(request, 'campaign/show.html',context)
