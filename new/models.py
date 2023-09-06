from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.urls import reverse

class New(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=500, blank=True)
    text = models.TextField(max_length=50000, blank=True)
    image = models.ImageField(upload_to='news', blank=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('new:new_detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('new')
        verbose_name_plural = _('news')
    
