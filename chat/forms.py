from django import forms
from django.utils.translation import gettext as _



class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label=_('Message'))
