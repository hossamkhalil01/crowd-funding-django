from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import campaign, donation

urlpatterns = [
    path('<int:campaign_id>', campaign.show, name='campaign_show'),
    path('donate/<int:campaign_id>', donation.donate, name='campaign_donate'),
]
