from django.db import models
from account.models import Profile
from django.urls import reverse


class Message(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000000)
    answer = models.CharField(max_length=1000000, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.message
    
    def get_absolute_url(self):
        return reverse("chat:chat_detail", args=[str(self.id)])
    
    class Meta:
        ordering = ['-date']

