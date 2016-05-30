from django.shortcuts import render
from models import books
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def book_list(request):

    query_list = books.objects.all()
    paginator = Paginator(query_list, 7)

    page = request.GET.get('page')
    try:
        query= paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    context = {'query':query}

    return render(request, "index.html",context)
