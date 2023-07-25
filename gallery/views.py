from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Image, Album
from .forms import AlbumForm, ImageUploadForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


def gallery(request):
    album = Album.objects.all()
    title = request.GET.get('title')
    print('title ,' , title)

    if title:
        album = album.filter(title=title)

    paginator = Paginator(album, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'gallery/gallery.html', {'page_obj': page_obj, 'album': album})

@login_required
def create_album(request, album_id=None):
    album = None
    if album_id:
        album = get_object_or_404(Album, id=album_id)
        form = AlbumForm(request.POST or None, request.FILES or None, instance=album)
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            album = form.save()
            messages.success(request, 'Album saved successfully.')
            return redirect('gallery:upload_image', album_id=album.id)
    else:
        form = AlbumForm()
    return render(request, 'gallery/create_album.html', {'form': form})


def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    image = Image.objects.filter(album=album)
    paginator = Paginator(image, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'gallery/album_detail.html', {'page_obj': page_obj, 'album': album, 'image': image})

@login_required
def upload_image(request, album_id):
    album = Album.objects.get(id=album_id)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.album = album
            image.image = request.FILES['image']
            image.uploaded_by = request.user.profile
            image.title = request.POST['title']
            image.description = request.POST['description']
            image.save()
            return redirect('gallery:album_detail', album_id=album.id)
    else:
        form = ImageUploadForm()
    return render(request, 'gallery/upload_image.html', {'form': form, 'album': album})


# class ImageListView(ListView):
#     model = Image
#     template_name = 'gallery/image_list.html'
#     context_object_name = 'images'

class ImageDetailView(DetailView):
    model = Image
    template_name = 'gallery/image_detail.html'
    context_object_name = 'image'

@login_required
def image_vote(request, id):
    user = request.user
    image = Image.objects.get(pk=id)
    if request.method == 'POST':
        if 'like' in request.POST:
            image.add_like(user.profile)
        elif 'dislike' in request.POST:
            image.add_dislike(user.profile)
    redirect_url = reverse('gallery:image_detail', args=[id])
    return redirect(redirect_url)