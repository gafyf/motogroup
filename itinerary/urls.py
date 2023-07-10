from django.urls import path
from .views import itineraries, ItineraryDetailView, create_itinerary, itinerary_vote

app_name = 'itinerary'

urlpatterns = [
    path('', itineraries, name='itineraries'),
    path('itinerary/<str:pk>/', ItineraryDetailView.as_view(), name='itinerary'),
    path('create_itinerary/', create_itinerary, name='create_itinerary'),
    path('update_itinerary/<str:pk>/', create_itinerary, name='update_itinerary'),
    path('itinerary_vote/<str:id>', itinerary_vote, name='itinerary_vote'),
]
