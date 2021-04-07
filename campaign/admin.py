from django.contrib import admin

from campaign.models import *

from .models import (Campaign, CampaignImage, CampaignReport, Category,
                     Donation, Rating)

# Register your models here.
# admin.site.register(Campaign)
admin.site.register(Category)
admin.site.register(CampaignReport)
admin.site.register(Rating)
admin.site.register(CampaignImage)
admin.site.register(Donation)

class Filter(admin.ModelAdmin):
    list_display = ("id" , "title" ,"is_featured")
    list_filter = ("is_featured","creation_date","category__label")
admin.site.register(Campaign,Filter)
