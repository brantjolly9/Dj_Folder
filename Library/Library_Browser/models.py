import datetime
from django.db import models
from django.utils.timezone import now as djNow
'''
Represents a frame in the database
has attributes to be called by Author.attr
Passed into views.py to change webpage
'''

class Author(models.Model):
    
    first_name = models.CharField(max_length=200, default=None)
    last_name = models.CharField(max_length=200, default=None)
    middle_initial = models.CharField(max_length=200, default=None)
    full_name = ''.join([first_name, middle_initial, last_name])
    # Lots of stuff

    def __str__(self):
        return self.last_name

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, default=None)
    # titleLong = models.CharField(max_length=400, default=None)
    pageCount = models.IntegerField(default=0)
    publishedDate = models.DateField(default=djNow)
    content = models.FileField(default='0')
    synopsis = models.CharField(max_length=1000, default='0')
    isbn = models.CharField(max_length=200, default='0')
    msrp = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    imageLink = models.CharField(max_length =200, default='No Link') ##! Put link
    

#     # Attaches the book obj to the author obj
    author = models.ManyToManyField(Author)
    def __str__(self):
        return self.title


