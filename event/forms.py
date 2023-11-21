from django import forms
from .models import Event
from django.utils.translation import gettext as _


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "country", "county", "town", "location", "start_time", "end_time", "image", "is_public", "is_private", "maximal_participants"]
        labels = {
            "title": _("Event name"),
            "description": _("Event description"),
            "country": _("Country"),
            "county": _("County"),
            "town": _("Town"),
            "location": _("Location"),
            "start_time": _("Start time"),
            "end_time": _("End time"),
            "image": _("Event image"),
            "is_public": _("Public"),
            "is_private": _("Private"),
            "maximal_participants": _("Maximal participants"),
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", 'required':'required', 'placeholder': _('Type the title of the event')}),
            "description": forms.Textarea(attrs={"class": "form-control", 'required':'required', 'placeholder': _('Type the description of the event')}),
            "country": forms.Select(attrs={"class": "form-control", 'required':'required', 'placeholder': _('Select the country of the event')}),
            "county": forms.TextInput(attrs={"class": "form-control", 'required':'required', 'placeholder': _('Type the county of the event')}),
            "town": forms.TextInput(attrs={"class": "form-control", 'placeholder': _('Type the town of the event')}),
            "location": forms.TextInput(attrs={"class": "form-control", 'required':'required', 'placeholder': _('Type Location')}),
            'start_time' : forms.DateTimeInput(attrs={"class": "form-control", 'required':'required', "type": "datetime-local"}, format="%d/%m/%Y %H:%M"),
            'end_time' : forms.DateTimeInput(attrs={"class": "form-control", 'required':'required', "type": "datetime-local"}, format="%d/%m/%Y %H:%M"),
            "image": forms.FileInput(attrs={"class": "form-control", 'required':'required', 'placeholder': _('Load image')}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input", 'placeholder': _('Public')}),
            "is_private": forms.CheckboxInput(attrs={"class": "form-check-input", 'placeholder': _('Private')}),
            "maximal_participants": forms.NumberInput(attrs={"class": "form-control", 'required':'False', 'placeholder': _('Enter the number of maximal participants ONLY IF REQUIRED')}),
        }
        
        help_texts = {
            "title": _(""),
            "description": _(""),
            "country": _(""),
            "county": _(""),
            "town": _(""),
            "location": _("OPEN GOOGLE MAPS - SEARCH - SHARE - INCLUDE MAP - COPY HTML CODE - PASTE HERE"),
            "start_time": _("Select the start date and time of the event"),
            "end_time": _("Select the end date and time of the event"),
            "image": _("Load the image of the event"),
            "is_public": _("Check if the event is public"),
            "is_private": _("Check if the event is private"),
            "maximal_participants": _(""),
        }


    # def save(self, commit=True):
    #     profile = super().save(commit=False)
    #     if self.instance.user:
    #         self.instance.user.first_name = self.cleaned_data['first_name']
    #         self.instance.user.last_name = self.cleaned_data['last_name']
    #         self.instance.user.profile.county = self.cleaned_data['county']
    #         self.instance.user.profile.town = self.cleaned_data['town']
    #         self.instance.user.profile.image = self.cleaned_data['image']
    #         self.instance.user.profile.description = self.cleaned_data['description']
    #         if commit:
    #             self.instance.user.save()
    #     if commit:
    #         profile.save()
    #     return profile