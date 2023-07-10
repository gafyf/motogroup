from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import views, get_user_model
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from typing import Any, Dict
from django.utils.decorators import method_decorator

from .models import Profile, User
from .forms import LoginForm, UserForm, PasswordResetForm, PasswordResetConfirmForm, PasswordChangeForm, ProfileUpdateForm


def activateEmail(request, user, to_email):
    mail_subject = _('Activate account')
    message = render_to_string('account/registration/activate_account.html', {
        'user': user.email,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, _(f'Go to your email address {to_email} to activate your account.'))
    else:
        messages.error(request, _(f'Email could not be sent to the address {to_email}, check if it is written correctly.'))

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data['email'])
            return redirect('account:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserForm()
    return render(request=request, template_name="account/registration/signup.html", context={'form':form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, _('Thank you for confirming the email. Now you can log in.'))
        return redirect('account:login')
    else:
        messages.error(request, _('The activation link is invalid or has already been used.'))
    return redirect('account:login')

class LoginView(views.LoginView):
    form_class = LoginForm
    template_name = "account/registration/login.html"

class LogoutView(views.LogoutView):
    template_name = "account/registration/logout.html"

class PasswordResetView(views.PasswordResetView):
    email_template_name = "account/registration/password_reset_email.html"
    form_class = PasswordResetForm
    template_name = "account/registration/password_reset_form.html"
    success_url = reverse_lazy("account:password_reset_done")

class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name = "account/registration/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")

class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "account/registration/password_reset_done.html"

class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = "account/registration/password_reset_complete.html"

class PasswordChangeView(views.PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("account:password_change_done")
    template_name= "account/registration/password_change_form.html"

def password_change_done(request):
    return render(request, 'account/registration/password_change_done.html')

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'account/registration/edit_profile.html'
    model = Profile
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("account:detail_profile")
    success_message = _('profile has been modified')

    def get_success_url(self):
        return reverse_lazy('account:detail_profile', kwargs={'pk': self.object.pk})
    
# class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     template_name = 'account/registration/edit_user.html'
#     model = User
#     form_class = UserUpdateForm
#     success_url = reverse_lazy("account:detail_profile")
#     success_message = _('user has been modified')

#     def get_success_url(self):
#         return reverse_lazy('account:detail_profile', kwargs={'pk': self.object.profile.pk})
    
#     def form_valid(self, form):
#         form.instance.profile.user = self.request.user
#         return super().form_valid(form)

def edit_user(request, pk):
    user = request.user
    template = 'account/registration/edit_user.html'
    return render(request, template, {'user': user})

class DeleteUser(SuccessMessageMixin, generic.DeleteView):
    model = User
    template_name = 'account/registration/delete_user.html'
    success_message = _('user has been deleted')
    success_url = reverse_lazy('account:login')

def delete_profile(request, pk):
    template = 'account/registration/delete_profile.html'
    if request.method == 'POST':
        profile = Profile.objects.get(pk=pk)
        profile.delete()
        messages.warning(request, _("profile has been deleted!"))
        if request.user.is_superuser and request.user.id is not profile.user.id:
            return redirect('account:signup')
        else:        
            return redirect('account:login')
    return render (request, template)

def detail_profile(request, pk):
    template = 'account/account/detail_profile.html'
    profile = Profile.objects.get(pk=pk)
    created_at = profile.created_at.strftime("%d/%m/%Y")
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            profile.image = form.cleaned_data['image']
            profile.save()
            return redirect('account:detail_profile', pk=pk)
    else:
        form = ProfileUpdateForm()
    context = {
        'profile': profile,
        'created_at': created_at,
        'form': form,
    }
    return render (request, template, context)