from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.urls import reverse
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create a user with the given email and password
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create a superuser with the given email and password
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Last Name'))
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('First Name'))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

def user_directory_path(instance, filename):
    return "users_images/{profile}/{filen}.jpg".format(profile=instance.user.first_name, file=filename, filen=instance.user.first_name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('User'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    county = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('County'))
    town = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Town'))
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name=_('Image'))
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    def __str__(self):
        if (self.user.first_name is True) and (self.user.last_name is True):
            return str(self.user.first_name) + " " + str(self.user.last_name)
        else:
            return str(self.user.email)

    def get_absolute_url(self):
        return reverse("account:edit_profile", args=[str(self.id)])

    class Meta:
        verbose_name_plural = _("Profils")
        ordering = ["-created_at"]       
