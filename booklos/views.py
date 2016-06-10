from django.shortcuts import render , get_object_or_404 , redirect
from models import books,categories
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def book_list(request):

    query_list = books.objects.all()
    category_list = categories.objects.all()
    paginator = Paginator(query_list, 8)

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
