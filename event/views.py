from typing import Any, Dict
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import EventForm
from .models import  Event
# from django.views.generic import FormView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

def event_list(request):
    events = Event.objects.all()

    created_by = request.GET.get('created_by')
    country = request.GET.get('country')
    if created_by:
        events = events.filter(created_by__user__email=created_by)
    elif country:
        events = events.filter(country=country)

    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'event/event_list.html', {'page_obj': page_obj, 'events': events})

class EventDetailView(DetailView):
    model = Event
    template_name = 'event/event.html'
    context_object_name = 'event'

@method_decorator(login_required, name='dispatch')
class EventFormView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "event/event_form.html"
    success_url = reverse_lazy("event:event_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user.profile
        self.object.save()
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('event:event_list')

    def get_initial(self) -> Dict[str, Any]:
        return super().get_initial()
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user.profile
        self.object.save()
        return super().form_valid(form)
    
    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     if self.request.user.is_authenticated:
    #         if not self.object.pk:
    #             self.object.created_by = self.request.user.profile
    #         self.object.updated_by = self.request.user.profile
    #     self.object.save()
    #     return super().form_valid(form)
    

    
@login_required
def event_vote(request, id):
    user = request.user
    event = Event.objects.get(pk=id)
    if request.method == 'POST':
        if 'like' in request.POST:
            event.add_like(user.profile)
        elif 'dislike' in request.POST:
            event.add_dislike(user.profile)
        if 'participate' in request.POST:
            event.participate(user.profile)
        elif 'interested' in request.POST:
            event.interested(user.profile)
    redirect_url = reverse('event:event', args=[id])
    return redirect(redirect_url)


# def event_participate(request, id):
#     event = Event.objects.get(pk=id)
#     user_profile = request.user.profile
    
#     if request.method == 'POST':
#         action = request.POST.get('action')
        
#         if action == 'participate':
#             event.participate(user_profile)
#         elif action == 'interested':
#             event.interested(user_profile)
        
#         # Return JSON response with the updated participation status
#         return JsonResponse({
#             'participating': user_profile in event.participants.all(),
#             'interested': user_profile in event.interested_participants.all()
#         })
    
#     return render(request, 'event/event.html', {'event': event})
