from django.shortcuts import render, redirect
from campaign.models import Category, Campaign, CampaignImage
from taggit.models import Tag
from ..forms import CampaignForm,ImageForm
from django.forms import modelformset_factory
import datetime

# Create your views here.


def create_campaign(request):
    ImageFormSet = modelformset_factory(CampaignImage, form=ImageForm, extra=2)

    if request.method == 'POST':
        form = CampaignForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,queryset=CampaignImage.objects.none())

        if form.is_valid() and formset.is_valid():
            new_form = form.save(commit=False)
            new_form.creator = request.user
            new_form.save()
            form.save_m2m()
            for form in formset.cleaned_data:
                # this helps to not crash if the user
                # do not upload all the photos
                if form:
                    image = form['path']
                    photo = CampaignImage(campaign=new_form, path=image)
                    photo.save()
            return redirect(f'/campaign/show/{new_form.id}')
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, 'campaign/campaign_create.html', context)
    else:

        form = CampaignForm()
        formset = ImageFormSet(queryset=CampaignImage.objects.none())
        context = {
            'form': form,
            'formset': formset,
        }
    return render(request, 'campaign/campaign_create.html', context)



