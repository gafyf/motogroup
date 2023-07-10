from django import forms
from .models import User, Profile
from .validators import validate_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):
    email = forms.EmailField(label='Email:', help_text=None, widget=forms.EmailInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': _('email@example.com')}))
    password1 = forms.CharField(label=_('Password:'), validators=[validate_password], help_text='The password must contain at least one special character and one capital letter.', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password", 'required': 'required', 'placeholder': _('Type your password...')}))
    password2 = forms.CharField(label=_('Password confirmation:'), help_text=None, strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password", 'required': 'required', 'placeholder': _('Password confirmation...')}))
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email:', help_text=None, widget=forms.EmailInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': _('email@example.com')}))
    password = forms.CharField(label=_('Password:'), help_text=None, strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password", 'required': 'required', 'placeholder': _('Password')}))

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email:', help_text=None, widget=forms.EmailInput(attrs={'class': 'form-control', 'autofocus': 'autofocus', 'required': 'required', 'placeholder': _('email@example.com')}))

class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password:'), validators=[validate_password], help_text='The password must contain at least one special character and one capital letter.', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password", 'autofocus': 'autofocus', 'required': 'required', 'placeholder': _('New Password')}))
    new_password2 = forms.CharField(label=_('Confirm New Password:'), help_text=None, strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password", 'required': 'required', 'placeholder': _('Confirm New Password')}))

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Password:'), help_text=None, strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password", 'autofocus': 'autofocus', 'required': 'required', 'placeholder': _('Password')}))
    new_password1 = forms.CharField(label=_('New Password:'), validators=[validate_password], help_text='The password must contain at least one special character and one capital letter.', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password", 'required': 'required', 'placeholder': _('New Password')}))
    new_password2 = forms.CharField(label=_('Confirm New Password:'), help_text=None, strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password", 'required': 'required', 'placeholder': _('Confirm New Password')}))

class ProfileUpdateForm(forms.ModelForm):
    last_name = forms.CharField(label=_('Last Name'), widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last Name')}), required=False)
    first_name = forms.CharField(label=_('First Name'), widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First Name')}), required=False)
    county = forms.CharField(label=_('County'), widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('County')}), required=False)
    town = forms.CharField(label=_('Town'), widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Town')}), required=False)
    image = forms.ImageField(label=_('Image'), widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': _('Image')}), required=False)
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'class': 'form-control custom-scroll', 'placeholder': _('Description')}), required=False)

    class Meta:
        model = Profile
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['county'].initial = self.instance.user.profile.county
            self.fields['town'].initial = self.instance.user.profile.town
            self.fields['image'].initial = self.instance.user.profile.image
            self.fields['description'].initial = self.instance.user.profile.description

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.instance.user:
            self.instance.user.first_name = self.cleaned_data['first_name']
            self.instance.user.last_name = self.cleaned_data['last_name']
            self.instance.user.profile.county = self.cleaned_data['county']
            self.instance.user.profile.town = self.cleaned_data['town']
            self.instance.user.profile.image = self.cleaned_data['image']
            self.instance.user.profile.description = self.cleaned_data['description']
            if commit:
                self.instance.user.save()
        if commit:
            profile.save()
        return profile
