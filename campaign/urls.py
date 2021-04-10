from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import campaign, donation, rating, report, create

urlpatterns = [
    path('show/<int:campaign_id>', campaign.show, name='campaign_show'),
    path('<int:campaign_id>/donate', donation.donate, name='campaign_donate'),
    path('<int:campaign_id>/report',
         report.campaign_report, name='campaign_report'),
    path('<int:campaign_id>/cancel',
         campaign.cancel, name='campaign_cancel'),
    path('<int:campaign_id>/rate', rating.rate, name='campaign_rate'),

    path('search', campaign.search, name='campaign_search'),

    path('search/all_results', campaign.search_all, name='campaign_search_all'),
    path('create', create.create_campaign, name='create_campaign'),
]
