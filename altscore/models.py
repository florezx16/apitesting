from django.db import models
import uuid

# Create your models here.
class DamagedSystem(models.Model):
    name = models.CharField(verbose_name='Damaged_system', max_length=50, unique=True)

    class Meta:
        verbose_name = "DamagedSystem"
        verbose_name_plural = "DamagedSystems"
        ordering = ['name']

    def __str__(self):
        return self.name

class SystemCode(models.Model):
    system = models.OneToOneField(to=DamagedSystem, verbose_name='System', on_delete=models.CASCADE)
    code = models.CharField(verbose_name='Code', max_length=50, unique=True)

    class Meta:
        verbose_name = "SystemCode"
        verbose_name_plural = "SystemCodes"
        ordering = ['code']

    def __str__(self):
        return self.code

class RequestLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system = models.ForeignKey(to=DamagedSystem, on_delete=models.CASCADE)
    createtime = models.DateTimeField(verbose_name='createtime', auto_now=True)
    
    class Meta:
        verbose_name = "RequestLog"
        verbose_name_plural = "RequestLogs"
        ordering = ['-createtime']
        
    def __str__(self):
        return str(self.id)