from django.shortcuts import render
from .models import New
from django.core.paginator import Paginator
# from .scraper import scraped_data
import requests
from django.core.files.images import ImageFile
from io import BytesIO


def new(request):
    print('scraped_data', scraped_data)
    
    for data in scraped_data:
        response = requests.get(data['article_image'])
        response.raise_for_status()
        # Get the image data in bytes
        image_data = response.content
        # Create a BytesIO object to create a Django File object
        image_file = ImageFile(BytesIO(image_data), name=f"{data['article_title']}.jpg")

        new = New(
            title=data['article_title'], 
            description=data['article_descritpion'], 
            text=data['article_block_text'], 
            link=data['link'],
            image=image_file,
            )
        new.save()
    
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
    new = New.objects.get(pk=pk)
    return render(request, 'new/new_detail.html', {'new': new})