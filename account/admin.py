from django.contrib import admin
# from django.contrib.admin.models import LogEntry
# from django.contrib.auth import get_user_model
from .models import Profile, User

# User = get_user_model()

# admin.site.register(LogEntry)
admin.site.register(Profile)
admin.site.register(User)
