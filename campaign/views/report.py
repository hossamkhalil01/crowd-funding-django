from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Campaign, CampaignReport


@login_required
def campaign_report(request, campaign_id):

    if request.method == "POST":
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        context = {"campaign": campaign}

        details = request.POST.get('details', '')
        subject = request.POST.get('subject', '')

        if details and subject and not is_spam(request.user.id, campaign_id):

            CampaignReport.objects.create(
                details=details, campaign_id=campaign_id, reporter_id=request.user.id)

    return redirect('campaign_show', campaign_id)


def is_spam(user, campaign):
    return (CampaignReport.objects.filter(reporter_id=user, campaign_id=campaign).count() >= 3)
