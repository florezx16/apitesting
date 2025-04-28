from django.db import models

# Create your models here.
class Client(models.Model):
    fullname = models.CharField(verbose_name='Full name', max_length=50)
    local_id = models.CharField(verbose_name='Local ID', max_length=50)
    income = models.FloatField(verbose_name='Monthly income')
    
