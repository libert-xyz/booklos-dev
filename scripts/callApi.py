import os
import sys
#from amazon.api import AmazonAPI
from django.core.exceptions import ObjectDoesNotExist
from booklos.models import books, categories
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
import datetime
from amazonproduct import API



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


def create_slug_category(instance, new_slug=None):
    slug = slugify(instance.category)
    if new_slug is not None:
        slug = new_slug
    qs = categories.objects.filter(category_slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug="%s-%s" %(slug, qs.first().id)
        return create_slug_category(instance, new_slug=new_slug)
    return slug

def run():

    api = API(locale='us')
    query = api.item_search('KindleStore', Keywords='free kindle books')
    #query = api.item_search('KindleStore', Keywords='top 100 free kindle ebooks')


    for i in query:

        #new = books.objects.get(id=i.asin)
        ##Search and Lookups
        try:
            updated = books.objects.get(id=str(i.ASIN))
            updated.check_status='Updated'
            updated.save()
            print i.ItemAttributes.Title.pyval.encode('utf8')


        except ObjectDoesNotExist:


            detail = api.item_lookup(str(i.ASIN))
            image = api.item_lookup(str(i.ASIN), ResponseGroup='Images')
            editorial_review = api.item_lookup(str(i.ASIN), ResponseGroup='EditorialReview')
            cat = api.item_lookup(str(i.ASIN),ResponseGroup='BrowseNodes')
            ##Database write
            b = books()
            c = categories()

            #c = categories()
            b.id=(i.ASIN)
            b.title=(i.ItemAttributes.Title.pyval.encode('utf8'))

            try :
                b.author=(i.ItemAttributes.Author.pyval.encode('utf8'))
            except:
                b.author=None

            b.url=(detail.Items.Item.DetailPageURL)
            ##Fix this , price change all the time
            b.price = 'Free'
            b.image =    (image.Items.Item.LargeImage.URL)
            b.image_medium = (image.Items.Item.MediumImage.URL)
            b.description = (editorial_review.Items.Item.EditorialReviews.EditorialReview.Content.pyval.encode('utf8'))
            b.slug = create_slug(b)

            try:
                #ca = categories()
                #c = categories(category=cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name)
                c.category=cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name
                c.category_slug = create_slug_category(c)
                #categories.category_slug = create_slug_category(c)
                c.save()
                b.category=c
                b.save()


            except:
                category_add = categories.objects.get(category=cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name)
                #b.category__categories=cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name
                b.save()
                category_add.books_set.add(b)
                b.save()
            #add2category = b.category_set.create(b)
