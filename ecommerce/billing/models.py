from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save

User = settings.AUTH_USER_MODEL


# Create your models here.
class BillingProfile(models.Model):
    user = models.OneToOneField(User, null = True, blank = True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

def user_created_receiver(sender, instance, created=False, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user = instance, email = instance.email)

pre_save.connect(user_created_receiver, sender=User)