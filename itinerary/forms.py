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
            # 'start_point': _('Start point'),
            # 'end_point': _('End point'),
            # 'distance': _('Distance'),
            # 'travel_time': _('Travel time'),
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
            # "start_point": forms.HiddenInput(attrs={'required':'required'}),
            # "waypoints": forms.HiddenInput(),
            # "end_point": forms.HiddenInput(attrs={'required':'required'}),
            # "distance": forms.HiddenInput(),
            # "travel_time": forms.HiddenInput(),
            "winter_stats": forms.CheckboxInput(attrs={"class": "form-check"}),
            # "maximal_participants": forms.NumberInput(attrs={"class": "form-control", 'required':'False', 'placeholder': _('Enter the number of maximal participants ONLY IF REQUIRED')}),
        }
        
        help_texts = {
            "country": _(""),
            'name': _('Type the name of the itinerary'),
            'description': _('Type the description of the itinerary'),
            'places_to_visit': _('Type the places to visit'),
            'places_to_eat': _('Type the places to eat'),
            'places_to_sleep': _('Type the places to sleep'),
            'places_to_sleep': _('Type the places to sleep'),
            # 'start_point': _('Type the start point'),
            # 'end_point': _('Type the end point'),
            # 'distance': _('Type the distance'),
            # 'travel_time': _('Type the travel time'),
            'winter_stats': _('Check if is closed during winter'),
            'image': _('Load image'),
        }
