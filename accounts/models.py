from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='static/images/default.jpg')

    def __str__(self):
        return self.user.username




# Comment out or remove the save_user_profile signal
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()
