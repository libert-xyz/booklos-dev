import os
import sys
from amazon.api import AmazonAPI
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


def run():

    api = API(locale='us')
    query = api.item_search('KindleStore', Keywords='free kindle books')


    for i in query:

        #new = books.objects.get(id=i.asin)
        ##Search and Lookups

        detail = api.item_lookup(str(i.ASIN))
        image = api.item_lookup(str(i.ASIN), ResponseGroup='Images')
        editorial_review = api.item_lookup(str(i.ASIN), ResponseGroup='EditorialReview')
        attributes = api.item_lookup(str(i.ASIN),ResponseGroup='ItemAttributes')
        cat = api.item_lookup(str(i.ASIN),ResponseGroup='BrowseNodes')
        ##Database write
        b = books()

        #c = categories()
        b.id=(i.ASIN)
        b.title=(i.ItemAttributes.Title.pyval.encode('utf8'))

        try :
            b.author=(i.ItemAttributes.Author.pyval.encode('utf8'))
            b.publisher = (attributes.Items.Item.ItemAttributes.Publisher)
            b.number_pages = (attributes.Items.Item.ItemAttributes.NumberOfPages)
        except:
            b.author=None
            b.publisher=None
            b.number_pages=None

        b.url=(detail.Items.Item.DetailPageURL)
        ##Fix this , price change all the time
        b.price = 'Free'
        b.image =    (image.Items.Item.LargeImage.URL)
        b.description = (editorial_review.Items.Item.EditorialReviews.EditorialReview.Content.pyval.encode('utf8'))
        b.slug = create_slug(b)

        try:
            c = categories(category=cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name)
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


        #try:
        #    b.objects.get(category__category=cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name)
        #    b.category = (cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name)

        #except:
        #    c.save()
        #    print 'halooooooooooooo'
            #b.category__category = c



        #try:
        #    b.objects.get(category__category=cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name)
            #category_search = categories.objects.get(category=cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name)
            #c = categories(category=category_search,book=b)
        #    category_search.book = b
        #    category_search.save()

        #except:
        #    c = categories(category=cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name,book=b)
        #    c.save()

        #c.category = (cat.Items.Item.BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name)
        #c.book = (b.id)


        #### if book exists update the price and the update timestamp

        #try:

        #    q = books.objects.get(id=i.asin)
            #if len(new) > 0:
        #    if i.price_and_currency[0] != None:
        #        q.price = i.price_and_currency[0]
        #    q.save()

        #except:
