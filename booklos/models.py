from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
import datetime

# Create your models here.


class categories(models.Model):
    category = models.CharField(max_length=20,unique=True)
    category_slug = models.SlugField(unique=True)
    #book = models.ForeignKey(books, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('booklos:category',kwargs={'slug': self.category_slug})

    def __str__(self):
        return self.category


    class Meta:
        ordering = ('category',)

class books(models.Model):

    id = models.CharField(max_length=20, primary_key=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.TextField()
    author = models.CharField(max_length=101, null=True)
    price = models.CharField(max_length=15)
    url = models.TextField()
    category = models.ForeignKey(categories,on_delete=models.CASCADE,null=True)

    #updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('booklos:detail',kwargs={'slug': self.slug})


    class Meta:
        ordering = ['-timestamp']
