from django.contrib import admin

from campaign.models import *

# Register your models here.

admin.site.register(Campaign)
admin.site.register(Category)
admin.site.register(CampaignReport)
admin.site.register(Rating)
admin.site.register(CampaignImage)
admin.site.register(Comment)
admin.site.register(CommentReport)
admin.site.register(Donation)
