from django.db import models
from account.models import Profile
from django.utils.translation import gettext as _
import uuid
from django.urls import reverse
import math

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

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(Profile, related_name='events', on_delete=models.CASCADE, null=True, blank=True)
    updated_by = models.ForeignKey(Profile, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    country = models.CharField(max_length=50, choices=COUNTRY, blank=True, verbose_name=_('Country'))
    county = models.CharField(max_length=50, blank=True, verbose_name=_('County'))
    town = models.CharField(max_length=50, blank=True, verbose_name=_('Town'))
    location = models.CharField(max_length=500, blank=True, verbose_name=_('Location'))
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.ImageField(upload_to='events', blank=True)
    is_public = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(Profile, related_name=_('liked_events'), blank=True)
    disliked_by = models.ManyToManyField(Profile, related_name=_('disliked_events'), blank=True)
    participants_number = models.IntegerField(default=0)
    participants = models.ManyToManyField(Profile, related_name=_('participants'), blank=True)
    interested_number = models.IntegerField(default=0)
    interested_participants = models.ManyToManyField(Profile, related_name=_('interested_participants'), blank=True)
    participants_required = models.PositiveIntegerField(default=0)
    maximal_participants = models.PositiveIntegerField(default=math.inf)

    def __str__(self):
        return str(self.title)

    def participate(self, user_profile):
        if user_profile in self.interested_participants.all():
            self.interested_participants.remove(user_profile)
            self.interested_number -= 1
        elif user_profile in self.participants.all():
            self.participants.remove(user_profile)
            self.participants_number -= 1
        else:
            self.participants.add(user_profile)
            self.participants_number += 1
        if self.participants_number >= self.maximal_participants:
            self.is_completed = True
        else:
            self.is_completed = False
        self.save()

    def show_participants_number(self):
        return self.participants_number

    def show_participants(self):
        return self.participants.all()

    def interested(self, user_profile):
        if user_profile in self.participants.all():
            self.participants.remove(user_profile)
            self.participants_number -= 1
        elif user_profile in self.interested_participants.all():
            self.interested_participants.remove(user_profile)
            self.interested_number -= 1
        else:
            self.interested_participants.add(user_profile)
            self.interested_number += 1
        self.save()

    def show_interested_number(self):
        return self.interested_number

    def show_interested_participants(self):
        return self.interested_participants.all()
        
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

    def get_image_url(self):
        return reverse("event:image", args=[str(self.id)])
    
    def get_absolute_url(self):
        return reverse("event:event", args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse("event:delete", args=[str(self.id)])
    
    def get_update_url(self):
        return reverse("event:update", args=[str(self.id)])
    
    def get_participants_url(self):
        return reverse("event:participants", args=[str(self.id)])
    
    def get_join_url(self):
        return reverse("event:join", args=[str(self.id)])
    
    def get_leave_url(self):
        return reverse("event:leave", args=[str(self.id)])
    
    def get_cancel_url(self):
        return reverse("event:cancel", args=[str(self.id)])
    
    def get_complete_url(self):
        return reverse("event:complete", args=[str(self.id)])
    
    def get_uncomplete_url(self):
        return reverse("event:uncomplete", args=[str(self.id)])

    class Meta:
        verbose_name_plural = _("Events")
        ordering = ["-created_at"]
