from django.db import models
from django.utils import timezone


# model post messages from a guest
class Message(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    text = models.TextField(max_length=5000, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def create(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name