from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    SORT_MAP = {
        'name': 'name',
        'min_price': 'price',
        'max_price': '-price',
    }
    template = 'catalog.html'
    sort_by = request.GET.get('sort')
    if sort_by == None:
        sort_by = 'name'
    context = {'phones': Phone.objects.all().order_by(SORT_MAP[sort_by])}
    return render(request, template, context)

def show_product(request, slug):
    template = 'product.html'
    context = {'phone':  Phone.objects.get(slug=slug)}
    return render(request, template, context)
