from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(verbose_name='Address', max_length=50, blank=True, null=True)
    phone_number = models.CharField(verbose_name='Phone number', max_length=50, blank=True, null=True)
    about_me = models.TextField(verbose_name='About me', max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"

    def __str__(self):
        return self.user

