from django.shortcuts import render , get_object_or_404 , redirect, render_to_response
from models import books,categories
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.context_processors import csrf

# Create your views here.


def book_list(request):


    #query_list={}
    #query_list.update(csrf(request))

    query_list = books.objects.all()
    category_list = categories.objects.all()
    paginator = Paginator(query_list, 11)

    page = request.GET.get('page')
    try:
        query= paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    context = {'query':query,'category_list':category_list}

    return render(request, "book_list.html",context)

def book_detail(request,slug=None):

    instance = get_object_or_404(books,slug=slug)
    context = {'instance':instance}

    return render(request,"book_detail.html",context)

def book_category(request, slug=None):

    c = get_object_or_404(categories,category_slug=slug)
    category_list = categories.objects.all()

    instance = books.objects.filter(category=c)


    paginator = Paginator(instance, 8)

    page = request.GET.get('page')
    try:
        query= paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)


    context = {'instance':query,'c':c,'category_list':category_list}
    return render(request, "book_category.html",context)

def book_search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']

    else:
        search_text = ''

    book = books.objects.filter(title__contains=search_text)

    return render_to_response('ajax_search.html', {'book': book})
