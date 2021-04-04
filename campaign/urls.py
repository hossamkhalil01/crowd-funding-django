from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import campaign

urlpatterns = [
    url(r'^(?P<campaign_id>\d+)/$', campaign.show, name='campaign_show'),
]
