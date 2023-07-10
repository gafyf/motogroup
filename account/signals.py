from .models import User, Profile
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext as _


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    print(_('You are sure to delete '), instance,'?')


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    print(_('User '), instance.user, instance, _('was deleted'))
    try:
        user = instance.user
        user.delete()
    except:
        pass

@receiver(pre_save, sender=Profile)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass

@receiver(post_delete, sender=Profile)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass



