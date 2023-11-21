from django.db import models
from account.models import Profile
import uuid
from django.utils.translation import gettext as _
from django.urls import reverse

COUNTRY = (
        (None, _('Select Country')),
        ('Italy', _('Italy')),
        ('Romania', _('Romania')),
        ('Switzerland', _('Switzerland')),
        ('Germany', _('Germany')),
        ('France', _('France')),
        ('Spain', _('Spain')),
        ('Portugal', _('Portugal')),
        ('Belgium', _('Belgium')),
        ('Austria', _('Austria')),
        ('Slovenia', _('Slovenia')),
        ('Hungary', _('Hungary')),
        ('Croatia', _('Croatia')),
        ('Bulgaria', _('Bulgaria')),
        ('Czech Republic', _('Czech Republic')),
        ('Poland', _('Poland')),
        ('Sweden', _('Sweden')),
        ('Norway', _('Norway')),
        ('Denmark', _('Denmark')),
)

class Itinerary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_itineraries')
    updated_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='updated_itineraries', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=20, choices=COUNTRY, blank=True, verbose_name=_('Country'))
    image = models.ImageField(upload_to='itineraries', blank=True)
    description = models.TextField(max_length=10000, blank=True)
    places_to_visit = models.TextField(max_length=1000, blank=True)
    places_to_eat = models.TextField(max_length=1000, blank=True)
    places_to_sleep = models.TextField(max_length=1000, blank=True)
    start_point = models.CharField(max_length=500)
    waypoints = models.CharField(max_length=1000, blank=True)
    end_point = models.CharField(max_length=500)
    distance = models.CharField(max_length=500)
    travel_time = models.CharField(max_length=100)
    winter_stats = models.BooleanField(default=False, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(Profile, related_name=_('liked_itineraries'), blank=True)
    disliked_by = models.ManyToManyField(Profile, related_name=_('disliked_itineraries'), blank=True)

    def __str__(self):
         return self.name
    
    def get_absolute_url(self):
        return reverse("itinerary:itinerary", args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse("itinerary:delete", args=[str(self.id)])
    
    def get_update_url(self):
        return reverse("itinerary:update", args=[str(self.id)])

    def add_like(self, user_profile):
        if self.is_disliked_by_user(user_profile):
                self.dislikes -= 1
                self.disliked_by.remove(user_profile)
        if self.is_liked_by_user(user_profile):
            self.likes -= 1
            self.liked_by.remove(user_profile)
        else:
            self.likes += 1
            self.liked_by.add(user_profile)
        self.save()

    def add_dislike(self, user_profile):
        if self.is_liked_by_user(user_profile):
                self.likes -= 1
                self.liked_by.remove(user_profile)
        if self.is_disliked_by_user(user_profile):
            self.dislikes -= 1
            self.disliked_by.remove(user_profile)
        else:
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
         verbose_name_plural = _('Itineraries')
         verbose_name = _('Itinerary')