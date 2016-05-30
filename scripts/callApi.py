import os
import sys
from amazon.api import AmazonAPI
from booklos.models import books
from django.conf import settings



#amz = os.environ.get('AMZ')
#amzscrt = os.environ.get('AMZSCRT')
#amzid = os.environ.get('AMZID')


def run():

    b = books()
    amazon = AmazonAPI(settings.AMZ, settings.AMZSCRT, settings.AMZID)
    query = amazon.search(Keywords='free kindle books', SearchIndex = 'KindleStore')

    for i in query:
        if i.asin not in b.id:
            b.id=(i.asin)
            b.title = (i.title)
            b.description = (i.editorial_review)
            b.image = (i.medium_image_url)
            b.author = (i.author)
            b.number_pages = (i.pages)
            b.publisher = (i.publisher)

            b.save()
