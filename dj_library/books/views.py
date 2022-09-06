from datetime import datetime
from django.shortcuts import render
from django.db.models import Max, Min
from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    sort_by = request.GET.get('sort')
    if sort_by == 'next':
        book_list = list(Book.objects.filter().order_by('pub_date').values())
    elif sort_by == 'prev':
        book_list = list(Book.objects.filter().order_by('-pub_date').values())
    else:
        book_list = list(Book.objects.filter().order_by('pub_date').values())
    i = 0
    for book in book_list:
        book_list[i]['pub_date_str'] = book['pub_date'].strftime('%Y-%m-%d')
        i += 1
    # context = {'book_list': Book.objects.all()}
    context = {'book_list': book_list}
    return render(request, template, context)

def books_view_by_date(request, filter_date):
    template = 'books/books_list.html'
    max_date = Book.objects.filter(pub_date__gt = datetime.strptime(filter_date, "%Y-%m-%d")).aggregate(Min('pub_date'))
    min_date = Book.objects.filter(pub_date__lt = datetime.strptime(filter_date, "%Y-%m-%d")).aggregate(Max('pub_date'))
    context = {
            'book_list': Book.objects.filter(pub_date = datetime.strptime(filter_date, "%Y-%m-%d")),
            'max_date': None,
            'min_date': None,
            }
    if max_date['pub_date__min'] != None:
        context['max_date'] = max_date['pub_date__min'].strftime('%Y-%m-%d')
    if min_date['pub_date__max'] != None:
        context['min_date'] = min_date['pub_date__max'].strftime('%Y-%m-%d')

    return render(request, template, context)