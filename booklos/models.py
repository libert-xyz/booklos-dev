from __future__ import unicode_literals

from django.db import models
from django.conf import settings


# Create your models here.

class books(models.Model):

    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.TextField()
    author = models.CharField(max_length=101)
    number_pages = models.IntegerField()
    publisher = models.CharField(max_length=100)
    price = models.CharField(max_length=10, default=True)
