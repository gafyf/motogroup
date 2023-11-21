from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Message
from django.utils.translation import gettext as _
from .forms import MessageForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator


def message_list(request):
    messages = Message.objects.filter(is_approved=True)

    # Create a Paginator object with 10 messages per page
    paginator = Paginator(messages, 10)

    # Get the current page number from the query parameters
    page_number = request.GET.get('page')

    # Get the Page object for the requested page number
    page_obj = paginator.get_page(page_number)

    user = request.user
    if user.is_authenticated:
        form = MessageForm()
        form.initial['email'] = user.email
        form.fields['email'].widget.attrs['readonly'] = True
        if user.first_name and user.last_name:
            form.initial['name'] = user.first_name + ' ' + user.last_name
            form.fields['name'].widget.attrs['readonly'] = True
        elif user.first_name:
            form.initial['name'] = user.first_name
            form.fields['name'].widget.attrs['readonly'] = True
        elif user.last_name:
            form.initial['name'] = user.last_name
            form.fields['name'].widget.attrs['readonly'] = True
        else:
            form.fields['name']
    else:
        form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.is_approved = False
            form.save()
            return redirect('guest:message_list')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    
    context = {'page_obj': page_obj, 'form':form}
    return render(request, "guest/message_list.html", context)


@login_required
@user_passes_test(lambda user: user.is_staff or user.is_superuser)
def message_approval(request):
    messages_to_approve = Message.objects.filter(is_approved=False)
    
    paginator = Paginator(messages_to_approve, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        approved_messages_ids = request.POST.getlist('approved_messages')
        for message_id in approved_messages_ids:
            message = Message.objects.get(pk=message_id)
            message.is_approved = True
            message.save()
        return redirect('guest:message_approval')
    return render(request, 'guest/message_approval.html', {'page_obj': page_obj, 'messages_to_approve': messages_to_approve})


@login_required
def message_vote(request, id):
    user = request.user
    message = Message.objects.get(pk=id)

    page_number = request.GET.get('page')

    if request.method == 'POST':
        if 'like' in request.POST:
            message.add_like(user)
        elif 'dislike' in request.POST:
            message.add_dislike(user)

    redirect_url = reverse('guest:message_list') + f'?page={page_number}#{id}'
    return redirect(redirect_url)
