from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .forms import ItineraryForm
from .models import Itinerary
from django.core.paginator import Paginator
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
import requests


def itineraries(request):
    itineraries = Itinerary.objects.all()
    country = request.GET.get('country')
    print('country ,' , country)

    if country:
        itineraries = itineraries.filter(country=country)

    paginator = Paginator(itineraries, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'itinerary/itineraries.html', {'page_obj': page_obj, 'itineraries': itineraries})


def get_location_name(lat, lng):
    api_key = settings.TOMTOM_API_KEY
    url = f'https://api.tomtom.com/search/2/reverseGeocode/{lat},{lng}.json?key={api_key}&radius=50'
    response = requests.get(url).json()
    if response.get('addresses'):
        addresses = response['addresses']
        if addresses:
            address = addresses[0]
            if address.get('address'):
                return address['address'].get('freeformAddress')
    return None

class ItineraryDetailView(DetailView):
    model = Itinerary
    template_name = 'itinerary/itinerary.html'
    context_object_name = 'itinerary'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itinerary = context['itinerary']

        start_point = itinerary.start_point.replace('LngLat', '')
        end_point = itinerary.end_point.replace('LngLat', '')
        waypoints = itinerary.waypoints.replace('LngLat', '')
        
        start_point = start_point.strip("()")
        end_point = end_point.strip("()")
        start_point = start_point.split(", ")
        end_point = end_point.split(", ")
        start_point_map = [start_point[1], start_point[0]]
        end_point_map = [end_point[1], end_point[0]]
        print('map points ,' ,   start_point_map, end_point_map)

        start_location = get_location_name(start_point[1], start_point[0])
        end_location = get_location_name(end_point[1], end_point[0])
        
        waypoints = waypoints.strip("['()']")  # Remove the square brackets
        waypoints = waypoints.split("),(")
        waypoints_latlng = []
        waypoints_locations = []
        for waypoint in waypoints:
            waypoint = waypoint.strip("()")
            waypoint = waypoint.split("),(")
            for point in waypoint:
                point = point.strip("()")
                point = point.split(", ")
                waypoint_latitude = point[1]
                waypoint_longitude = point[0]
                waypoint_location = get_location_name(waypoint_latitude, waypoint_longitude)
                waypoints_locations.append(waypoint_location)
                waypoints_latlng.append(f"{waypoint_latitude}, {waypoint_longitude}")
        print(waypoints_latlng)

        # Add the location names to the context
        context['start_point_map'] = start_point_map
        context['end_point_map'] = end_point_map
        context['waypoints_latlng'] = waypoints_latlng
        context['start_location'] = start_location
        context['end_location'] = end_location
        context['waypoints_locations'] = waypoints_locations
        context['api_key'] = settings.TOMTOM_API_KEY

        return context


@login_required
def create_itinerary(request, pk=None):
    itinerary = None
    api_key = settings.TOMTOM_API_KEY
    print('api get tom create itinerary', api_key)

    if pk:
        itinerary = get_object_or_404(Itinerary, id=pk)
        form = ItineraryForm(request.POST or None, request.FILES or None, instance=itinerary)
    else:
        form = ItineraryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            itinerary = form.save(commit=False)
            if pk:
                itinerary.updated_by = request.user.profile
            else:
                itinerary.created_by = request.user.profile
            itinerary.start_point = request.POST.get('start_point')
            itinerary.end_point = request.POST.get('end_point')
            itinerary.waypoints = request.POST.getlist('waypoints')
            itinerary.distance = request.POST.get('distance')
            itinerary.travel_time = request.POST.get('travel_time')
            itinerary.country = form.cleaned_data['country']
            itinerary.name = form.cleaned_data['name']
            itinerary.image = form.cleaned_data['image']
            itinerary.description = form.cleaned_data['description']
            itinerary.places_to_visit = form.cleaned_data['places_to_visit']
            itinerary.places_to_eat = form.cleaned_data['places_to_eat']
            itinerary.places_to_sleep = form.cleaned_data['places_to_sleep']
            itinerary.winter_stats = form.cleaned_data['winter_stats']
            itinerary.save()

            messages.success(request, 'Itinerary saved successfully.')
            return redirect('itinerary:itineraries')
        else:
            return JsonResponse({'error': form.errors}, status=400)
        
    return render(request, 'itinerary/create_itinerary.html', {'form': form, 'api_key': api_key})


@login_required
def itinerary_vote(request, id):
    user = request.user
    itinerary = Itinerary.objects.get(pk=id)
    if request.method == 'POST':
        if 'like' in request.POST:
            itinerary.add_like(user.profile)
        elif 'dislike' in request.POST:
            itinerary.add_dislike(user.profile)
    redirect_url = reverse('itinerary:itinerary', args=[id])
    return redirect(redirect_url)
