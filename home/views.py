from django.shortcuts import render;
from campaign.models import Campaign;
from django.db.models import Avg;

# Create your views here.
def index(request):
  campaigns = Campaign.objects.annotate(avg_rate=Avg('ratings__value')).order_by('-avg_rate')[:5]
  return render(request, 'home/index.html', {'campaigns': campaigns})