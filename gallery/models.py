from django.db import models
from account.models import Profile
import uuid
from django.utils.translation import gettext as _
from django.urls import reverse


def get_image_upload_path(instance, filename):
    return f'gallery/albums/{instance.album.title}/{filename}'

    
class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("gallery:album_detail", args=[str(self.id)])
    
class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name=_('uploaded_by'), verbose_name=_('Uploaded By'))
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=10000, blank=True)
    image = models.ImageField(upload_to=get_image_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(Profile, related_name=_('liked_images'), blank=True)
    disliked_by = models.ManyToManyField(Profile, related_name=_('disliked_images'), blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("gallery:image_detail", args=[str(self.id)])
    
    def add_like(self, user_profile):
        if self.is_disliked_by_user(user_profile):
                self.dislikes -= 1
                self.disliked_by.remove(user_profile)
        if self.is_liked_by_user(user_profile):
            # User already liked the message, remove the like
            self.likes -= 1
            self.liked_by.remove(user_profile)
        else:
            # User hasn't liked the message, add the like and remove dislike if exists
            self.likes += 1
            self.liked_by.add(user_profile)
        self.save()

    def add_dislike(self, user_profile):
        if self.is_liked_by_user(user_profile):
                self.likes -= 1
                self.liked_by.remove(user_profile)
        if self.is_disliked_by_user(user_profile):
            # User already disliked the message, remove the dislike
            self.dislikes -= 1
            self.disliked_by.remove(user_profile)
        else:
            # User hasn't disliked the message, add the dislike and remove like if exists
            self.dislikes += 1
            self.disliked_by.add(user_profile)
        self.save()

    def is_liked_by_user(self, user_profile):
        if self.liked_by.filter(id=user_profile.id).exists():
            self.disliked_by.remove(user_profile)
        return self.liked_by.filter(id=user_profile.id).exists()

    def is_disliked_by_user(self, user_profile):
        if self.disliked_by.filter(id=user_profile.id).exists():
            self.liked_by.remove(user_profile)
        return self.disliked_by.filter(id=user_profile.id).exists()
    
    class Meta:
         ordering = ['-created_at']
         verbose_name_plural = _('Images')
         verbose_name = _('Image')