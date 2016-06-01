from django.conf.urls import url
from django.contrib import admin
from views import *

urlpatterns = [

       url(r'^$', book_list,name='list'),
       url(r'^(?P<slug>[\w-]+)/$', book_detail,name='detail'),


         ]
