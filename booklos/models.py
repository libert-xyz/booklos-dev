from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
import datetime

# Create your models here.

class books(models.Model):

    id = models.CharField(max_length=20, primary_key=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.TextField()
    author = models.CharField(max_length=101, null=True)
    number_pages = models.IntegerField(null=True)
    publisher = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=15)
    url = models.TextField()
    reviews = models.TextField()

    #updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('booklos:detail',kwargs={'slug': self.slug})

#def create_slug(instance, new_slug=None):
#    slug = slugify(instance.title)
#    if new_slug is not None:
#        slug = new_slug
#    qs = books.objects.filter(slug=slug).order_by("-id")
#    exists = qs.exists()
#    if exists:
#        new_slug = "%s-%s" %(slug, qs.first().id)
#        return create_slug(instance, new_slug=new_slug)

#    return slug

#def pre_save_post_receiver(sender, instance, *args, **kwargs):
#    if not instance.slug:
#        instance.slug = create_slug(instance)

#    if not instance.updated:
#        instance.updated = datetime.datetime.now()

#    if not instance.timestamp:
#        instance.timestamp = datetime.datetime.now()

#pre_save.connect(pre_save_post_receiver, sender=books)
