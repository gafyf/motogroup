from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('event_list/', views.event_list, name='event_list'),
    path('event_form/', views.EventFormView.as_view(), name='event_form'),
    path('event_update/<str:pk>/', views.EventUpdateView.as_view(), name='event_update'),
    path('event/<str:pk>/', views.EventDetailView.as_view(), name='event'),
    path('event_vote/<str:id>', views.event_vote, name='event_vote'),
]
