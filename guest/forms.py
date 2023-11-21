from django import forms
from .models import Message
from django.utils.translation import gettext_lazy as _

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'email', 'text')
        labels = {
            'name': _('Name'),
            'email': _('Email'),
            'text': _('Message'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': _('Type your name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': _('Type your email')}),
            'text': forms.Textarea(attrs={'class': 'form-control custom-scroll', 'rows': '5', 'cols': '40', 'required': 'required', 'placeholder': _('Type your message...')}),
        }