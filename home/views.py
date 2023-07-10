from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.translation import gettext as _


def home(request):
    template = 'home/home.html'
    title = _('Home')
    context = {
        'title': title,
    }
    response = render(request, template, context)
    return response

def search(request):
    template = 'home/search.html'
    title = _('Search')
    context = {
        'title': title,
    }
    response = render(request, template, context)
    return response
