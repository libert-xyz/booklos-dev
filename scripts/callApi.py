import os
import sys
from amazon.api import AmazonAPI
from booklos.models import books
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
import datetime


#amz = os.environ.get('AMZ')
#amzscrt = os.environ.get('AMZSCRT')
#amzid = os.environ.get('AMZID')

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = books.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)

    return slug


def run():

    b = books()
    amazon = AmazonAPI(settings.AMZ, settings.AMZSCRT, settings.AMZID)
    query = amazon.search(Keywords='free kindle books', SearchIndex = 'KindleStore')




    for i in query:

        #new = books.objects.get(id=i.asin)
        b = books()

        #if book exists update the price and the update timestamp

        try:

            q = books.objects.get(id=i.asin)
            #if len(new) > 0:
            if i.price_and_currency[0] != None:
                q.price = i.price_and_currency[0]
            q.save()

        except:


            b.id=(i.asin)
            b.title = (i.title)
            b.description = (i.editorial_review)
            b.image = (i.large_image_url)
            b.author = (i.author)
            b.number_pages = (i.pages)
            b.publisher = (i.publisher)
            b.price = 'Free'
            b.url = (i.offer_url)
            b.reviews = (i.reviews[1])
            b.slug = create_slug(b)

            b.save()
