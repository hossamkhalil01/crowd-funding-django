from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import campaign, donation

urlpatterns = [
    path('show/<int:campaign_id>', campaign.show, name='campaign_show'),
    path('<int:campaign_id>/donate', donation.donate, name='campaign_donate'),
    path('<int:campaign_id>/comment', campaign.comment, name='campaign_comment'),
    path('<int:campaign_id>/reply/<int:comment_id>', campaign.reply, name='campaign_reply'),
]
