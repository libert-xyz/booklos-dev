from django.conf.urls import url
from django.contrib import admin
from views import *

urlpatterns = [

       url(r'^$', book_list,name='list'),
       url(r'^book/(?P<slug>[\w-]+)/$', book_detail,name='detail'),
       url(r'^category/(?P<slug>[\w-]+)/$', book_category,name='category'),
       url(r'^search/$', book_search),

         ]
