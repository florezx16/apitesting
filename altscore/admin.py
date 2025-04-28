from django.contrib import admin
from .models import DamagedSystem, SystemCode, RequestLog

# Register your models here.
class DamagedSystemAdmin(admin.ModelAdmin):
    list_display = ['name']
    
class SystemCodeAdmin(admin.ModelAdmin):
    list_display = ['system','code']
    
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ['id','system','createtime']
    search_fields = ['id','system']
    
admin.site.register(DamagedSystem,DamagedSystemAdmin)
admin.site.register(SystemCode,SystemCodeAdmin)
admin.site.register(RequestLog,RequestLogAdmin)
