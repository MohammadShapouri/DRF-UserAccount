from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import UserAccountProfilePicture



@receiver(pre_delete, sender=UserAccountProfilePicture)
def setNewDefaultProfilePicture(sender, instance, *args, **kwargs):
    if instance.is_default_pic == True:
        latestUserAccountProfilePicture = UserAccountProfilePicture.objects.latest('creation_date')
        latestUserAccountProfilePicture.is_default_pic = True
        latestUserAccountProfilePicture.save()



@receiver(pre_save, sender=UserAccountProfilePicture)
def unsetOldDefaultProfilePicture(sender, instance, *args, **kwargs):
    if instance.is_default_pic == True:
        UserAccountProfilePicture.objects.filter(user=instance.user, is_default_pic=True).update(is_default_pic=False)
