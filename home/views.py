from campaign.models import Campaign
from django.db.models import Avg
from django.shortcuts import render


# Create your views here.
def index(request):
  highest_rated_campaigns = Campaign.objects.annotate(avg_rate=Avg('ratings__value')).order_by('-avg_rate')[:5]
  latest_campaigns = Campaign.objects.order_by('-creation_date')[:5]
  featured_campaigns = Campaign.objects.filter(is_featured=1)
  print("********************************")
  print(latest_campaigns)
  return render(request, 'home/index.html', {'highest_rated_campaigns': highest_rated_campaigns, 
  'latest_campaigns': latest_campaigns, 'featured_campaigns': featured_campaigns,})
