from django.urls import path
from .views import ImageDetailView, gallery, create_album, album_detail, upload_image, image_vote

app_name = 'gallery'

urlpatterns = [
    path('gallery/', gallery, name='gallery'),
    # path('', ImageListView.as_view(), name='image_list'),
    path('<str:pk>/', ImageDetailView.as_view(), name='image_detail'),
    path('', create_album, name='create_album'),
    path('update_album/<str:album_id>/', create_album, name='update_album'),
    path('album_detail/<str:album_id>/', album_detail, name='album_detail'),
    path('upload_image/<str:album_id>/', upload_image, name='upload_image'),
    path('image_vote/<str:id>', image_vote, name='image_vote'),
]
