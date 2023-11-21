from django.shortcuts import render
from .models import New
from django.core.paginator import Paginator
from .run_scraping import run_file_periodically


def new(request):
    news = New.objects.all()
    title = request.GET.get('title')
    print('title ,' , title)

    if title:
        news = news.filter(title__icontains=title)

    paginator = Paginator(news, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'new/new.html', {'page_obj': page_obj, 'news': news})


def new_detail(request, pk):
    run_file_periodically()
    new = New.objects.get(pk=pk)
    return render(request, 'new/new_detail.html', {'new': new})
