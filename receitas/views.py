from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from utils.pagination import make_pagination
from receitas.models import  Receita

QTY_PAGES = 6 # multiplo de 3
ITEMS_PAGE = 8 # Obrigatorio ser numero par
#===========================================================================




def home(request):
    receitas = get_list_or_404(
        Receita.objects.filter(
            is_published=True,
            ).order_by('-id'))

    page_obj, pagination_range = make_pagination(request, receitas, QTY_PAGES, ITEMS_PAGE)

    context = {'receitas': page_obj, 'pagination_range': pagination_range }
    return render(request, 'receitas/pages/home.html', context)


def category(request, category_id):
    receitas = get_list_or_404(
        Receita.objects.filter(
            category__id=category_id, 
            is_published=True
            ).order_by('-id'))
    

    page_obj, pagination_range = make_pagination(request, receitas, QTY_PAGES, ITEMS_PAGE)

    context = {'receitas':page_obj, 
               'pagination_range':pagination_range,
               'titulo': 'Categoria | ' + f'{receitas[0].category.name}'}
    return render(request, 'receitas/pages/category.html', context)


def receitas(request, id):
    receita = get_object_or_404(Receita, pk=id, is_published=True,)
    context = {'receita': receita, 'is_detail_page': True}
    return render(request, 'receitas/pages/receita_view.html', context)


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()
    
    receitas = Receita.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, receitas, QTY_PAGES, ITEMS_PAGE)

    context = {'page_title': f'Pesquisa por "{search_term}" |',
               'search_term': search_term,
               'pagination_range':pagination_range,
               'receitas': page_obj,
               'additional_url_query': f'&q={search_term}'}
    return render(request, 'receitas/pages/search.html', context)