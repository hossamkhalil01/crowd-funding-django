from django.shortcuts import render, redirect
from campaign.models import Category,Campaign
from taggit.models import Tag
import datetime

# Create your views here.


def create_campaign(request):
    uploadCover(request, Campaign.objects.last())
    # selectTags(request.POST.get('tags').split(), Campaign.objects.last())
    
    if request.method == "GET":
        category = Category.objects.all()
        tags = Campaign.tags.most_common()[:4]
        return render(request, 'campaign/campaign_create.html',{'category':category})
    else:
        campaign = Campaign.objects.create(
            title= request.POST.get('title'),
            details= request.POST.get('details'),
            category_id = request.POST.get('category'),
            target= request.POST.get('target'),
            start_date = request.POST.get('start_date'),
            end_date= request.POST.get('end_date'),
            creator = request.user,
            
        )

        if  campaign.clean():
            campaign.save()
            return redirect('home')
        else:
            return render(request, 'campaign/create.html', {'new_campaign': campaign, 'category': category})

        

def uploadCover(cover, campaign):
    for file in cover.FILES.getlist('cover'):
        cover = Campaign.objects.create(campaign =  campaign, cover = file)


# def tagged(request):

#     for tag_name in tags:
#         newTag = tags.objects.create(campaign = campaign, tags = tag_name)