from django.urls import path
from .views import  message_list,  message_vote, message_approval


app_name = 'guest'

urlpatterns = [
    path('message_list/', message_list, name='message_list'),
    path('message_approval/', message_approval, name='message_approval'),
    path('message_vote/<str:id>', message_vote, name='message_vote'),
]
