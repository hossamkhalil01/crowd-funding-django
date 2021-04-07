import datetime
from django.contrib import messages
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
from ..models import Campaign
from taggit.models import Tag


def show(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    images = campaign.images.all()
    average_rating = campaign.ratings.all().aggregate(Avg('value'))[
        'value__avg']

    # return user rating if found
    user_rating = 0

    if request.user.is_authenticated:
        prev_rating = campaign.ratings.filter(user_id=request.user.id)

        if prev_rating:
            user_rating = prev_rating[0].value

    if average_rating is None:
        average_rating = 0
    donations = campaign.donations.all().aggregate(Sum('amount'))[
        'amount__sum']
    if donations is None:
        donations = 0
    tags = campaign.tags.all()
    delta = timezone.now() - campaign.start_date

    context = {'campaign_info': campaign, 'images': images, 'rating': average_rating*20,
               'tags': tags, 'donations': donations, 'days': delta.days, 'user_rating': user_rating, 'rating_range': range(5, 0, -1)}

    return render(request, 'campaign/show.html', context)


def search(request):

    # respond to ajax requests only
    if request.is_ajax and request.method == "GET":

        # get the searching key
        search_key = request.GET.get('key')

        # return matched campaigns
        matched_by_title = Campaign.objects.filter(
            title__icontains=search_key)[:5]
        # TODO: get the tags taht have the key

        # return matched tags
        tags = Tag.objects.filter(name__icontains=search_key)[:5]

        # get list of tags ids
        tags_ids = []
        for tag in tags:
            tags_ids.append(tag.id)

        matched_by_tags = Campaign.objects.filter(tags__id__in=tags_ids)

        # serialize the result
        matched_by_title = serializers.serialize('json', matched_by_title)
        matched_by_tags = serializers.serialize('json', matched_by_tags)

        return JsonResponse({"by_title": matched_by_title, "by_tags": matched_by_tags})
