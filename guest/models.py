from django.db import models
from django.utils.translation import gettext as _
import uuid
from account.models import User


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    text = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name=_('liked_messages'), blank=True)
    disliked_by = models.ManyToManyField(User, related_name=_('disliked_messages'), blank=True)
                                  
    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return f"/message/{self.id}"
    

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
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        