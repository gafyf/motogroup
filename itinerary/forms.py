from django import forms
from .models import Itinerary
from django.utils.translation import gettext as _


class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['country', 'name', 'image', 'description', 'places_to_visit', 'places_to_eat', 'places_to_sleep', 'winter_stats']
        labels = {
            'country': _('Country'),
            'name': _('Name'),
            'image': _('Image'),
            'description': _('Description'),
            'places_to_visit': _('Places to visit'),
            'places_to_eat': _('Places to eat'),
            'places_to_sleep': _('Places to sleep'),
            'winter_stats': _('Winter stats'),
        }
        widgets = {
            "country": forms.Select(attrs={"class": "form-control", 'required':'required', 'placeholder': _('Select the country')}),
            "name": forms.TextInput(attrs={"class": "form-control", 'required':'required', 'placeholder': _('Type the name of the itinerary')}),
            "description": forms.Textarea(attrs={"class": "form-control", 'required':'required', 'placeholder': _('Type the description of the itinerary')}),
            "places_to_visit": forms.Textarea(attrs={"class": "form-control", 'placeholder': _('Type the places to visit')}),
            "places_to_eat": forms.Textarea(attrs={"class": "form-control", 'placeholder': _('Type the places to eat')}),
            "places_to_sleep": forms.Textarea(attrs={"class": "form-control", 'placeholder': _('Type the places to sleep')}),
            "image": forms.FileInput(attrs={"class": "form-control", 'placeholder': _('Load image')}),
            "winter_stats": forms.CheckboxInput(attrs={"class": "form-check"}),
        }
        
        help_texts = {
            "country": _(""),
            'name': _('Type the name of the itinerary'),
            'description': _('Type the description of the itinerary'),
            'places_to_visit': _('Type the places to visit'),
            'places_to_eat': _('Type the places to eat'),
            'places_to_sleep': _('Type the places to sleep'),
            'places_to_sleep': _('Type the places to sleep'),
            'winter_stats': _('Check if is closed during winter'),
            'image': _('Load image'),
        }
