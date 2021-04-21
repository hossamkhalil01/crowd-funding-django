from campaign.models import Campaign, Category
from django.db.models import Avg
from django.shortcuts import get_object_or_404, render

# Create your views here.


def index(request):

    highest_rated_campaigns = Campaign.objects.annotate(
        avg_rate=Avg('ratings__value')).order_by('-avg_rate')[:5]
    latest_campaigns = Campaign.objects.order_by('-creation_date')[:8]
    featured_campaigns = Campaign.objects.filter(is_featured=1)
    categories = Category.objects.all()
    return render(request, 'home/index.html',
                  {'highest_rated_campaigns': highest_rated_campaigns,
                   'latest_campaigns': latest_campaigns, 'featured_campaigns': featured_campaigns,
                   'categories': categories})


def category(request, categoty_id):

    if request.method == "GET":

        categories = Category.objects.all()
        category = get_object_or_404(Category, id=categoty_id)
        campaigns = Campaign.objects.filter(category=categoty_id)

    return render(request, 'home/category.html', {"campaigns": campaigns,
                                                  "category": category, "categories": categories})


def error_404(request, exception):
    data = {}
    return render(request, 'home/404.html', data)
