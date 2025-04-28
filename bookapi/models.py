from django.db import models

# Create your models here.
class Book(models.Model):
    class BookGenres(models.IntegerChoices):
        horror = (1,'Horror')
        romance = (2,'Romance')
        scific = (3,'Science fiction')
        fantansy = (4,'Fantasy')
        
    class BookStatus(models.IntegerChoices):
        enable = (1,'Enable')
        disable = (0,'Disable')
    
    isbn = models.CharField(max_length=50,unique=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publish_date = models.DateField()
    pages_number = models.IntegerField()
    genre = models.IntegerField(choices=BookGenres.choices)
    status = models.IntegerField(choices=BookStatus.choices,default=BookStatus.enable)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    
    class Meta():
        ordering = ['-updatetime','author']
    
    def __str__(self):
        return self.isbn
    
    
    