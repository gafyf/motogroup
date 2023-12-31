from django import forms
from .models import Album, Image
from django.utils.translation import gettext as _


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'title', 'description']

        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control", 'placeholder': _('Load image')}),
            "title": forms.TextInput(attrs={"class": "form-control",  'placeholder': _('Type the title of the image')}),
            "description": forms.Textarea(attrs={"class": "form-control", 'placeholder': _('Type the description of the image')}),
        }
   
