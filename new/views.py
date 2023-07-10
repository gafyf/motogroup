from django.shortcuts import render

def new(request):
    return render(request, 'new.html')