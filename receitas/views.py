import os
from typing import List

from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from utils.pagination import make_pagination
from receitas.models import  Receita

POR_PAGINA = 6 # multiplo de 3
PAGINA_POR_TELA = 6 # Obrigatorio ser numero par
#===========================================================================

class RecipeListViewBase(ListView):
    model = Receita
    context_object_name = 'receitas'
    ordering = ['-id']
    template_name = 'receitas/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True,)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, ctx.get('receitas'), POR_PAGINA, PAGINA_POR_TELA)

        ctx.update({'receitas': page_obj, 'pagination_range': pagination_range})
        return ctx
#===========================================================================

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'receitas/pages/home.html'
#===========================================================================
    
class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'receitas/pages/category.html'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(category_id = self.kwargs.get('category_id'))
        return qs
#===========================================================================
    
class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'receitas/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ))
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx

        
#===========================================================================

class RecipeDetail(DetailView):
    model = Receita
    context_object_name = 'receitas'
    template_name = 'receitas/pages/receita_view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs


    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({'is_detail_page': True})

        return ctx


#############################################################################
#############################################################################  
def home(request):
    receitas = get_list_or_404(
        Receita.objects.filter(
            is_published=True,
            ).order_by('-id'))

    page_obj, pagination_range = make_pagination(request, receitas, POR_PAGINA, PAGINA_POR_TELA)

    context = {'receitas': page_obj, 'pagination_range': pagination_range }
    return render(request, 'receitas/pages/home.html', context)


def category(request, category_id):
    receitas = get_list_or_404(
        Receita.objects.filter(
            category__id=category_id, 
            is_published=True
            ).order_by('-id'))
    

    page_obj, pagination_range = make_pagination(request, receitas, POR_PAGINA, PAGINA_POR_TELA)

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

    page_obj, pagination_range = make_pagination(request, receitas, POR_PAGINA, PAGINA_POR_TELA)

    context = {'page_title': f'Pesquisa por "{search_term}" |',
               'search_term': search_term,
               'pagination_range':pagination_range,
               'receitas': page_obj,
               'additional_url_query': f'&q={search_term}'}
    return render(request, 'receitas/pages/search.html', context)