import os
from typing import List
from django.db.models import Q
from django.http.response import Http404
from django.views.generic import ListView, DetailView
from utils.pagination import make_pagination
from django.http import JsonResponse
from receitas.models import  Receita

QTY_PAGES = 6 # multiplo de 3
ITEMS_PAGE = 4 # Obrigatorio ser numero par

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

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
        page_obj, pagination_range = make_pagination(self.request, ctx.get('receitas'), QTY_PAGES, ITEMS_PAGE)

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
    context_object_name = 'receita'
    template_name = 'receitas/pages/receita_view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs


    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({'is_detail_page': True})

        return ctx
