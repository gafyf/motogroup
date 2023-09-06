from django.urls import path
from . import views

app_name = 'new'

urlpatterns = [
    path('', views.new, name='new'),
    path('new_detail/<str:pk>/', views.new_detail, name='new_detail'),
]
