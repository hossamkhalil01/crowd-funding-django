from django.db.models import Avg, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Campaign, CampaignImage, Rating


def show(request, campaign_id):
    return render(request, 'campaign/show.html')
