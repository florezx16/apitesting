from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','isbn','title','author','genre','publish_date','status']
    readonly_fields = ['createtime','updatetime']
    list_filter = ['status','genre']
    ordering = ['title','updatetime']
    search_fields = ['title','author','genre','isbn']

admin.site.register(Book,BookAdmin)