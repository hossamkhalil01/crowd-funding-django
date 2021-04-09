
from django import forms
from django.forms import ModelForm
from django.utils import timezone

from .models import Campaign, CampaignImage


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'details', 'target','start_date', 'end_date', 'category', 'tags']
        

    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['details'].widget.attrs.update({'class': 'form-control'})
        self.fields['target'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['tags'].widget.attrs.update({'class': 'form-control'})



    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date <= start_date:
            msg = u"End date should be greater than start date."
            self._errors["end_date"] = self.error_class([msg])


class ImageForm(forms.ModelForm):
    class Meta:
        model = CampaignImage
        fields = ['path', ]
