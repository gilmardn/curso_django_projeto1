from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
#from utils.receitas.factory import make_receita
from receitas.models import  Receita


def home(request):
    receitas = get_list_or_404(Receita.objects.filter(is_published=True,).order_by('-id'))
    #context = {'receitas':make_receita() for _ in range(10)}
    context = {'receitas':receitas}
    return render(request, 'receitas/pages/home.html', context)

def category(request, category_id):
    receitas = get_list_or_404(
        Receita.objects.filter(
            category__id=category_id, 
            is_published=True
            ).order_by('-id'))
    # context = {'receitas':make_receita() for _ in range(10)}
    context = {'receitas':receitas, 'titulo': 'Categoria | ' + f'{receitas[0].category.name}'}
    return render(request, 'receitas/pages/category.html', context)


def receitas(request, id):
   # receita = Receita.objects.filter(pk=id, is_published=True).order_by('-id').first
    receita = get_object_or_404(Receita, pk=id, is_published=True,)
    context = {'receita': receita, 'is_detail_page': True}
    return render(request, 'receitas/pages/receita_view.html', context)


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()
    
    receitas = Receita.objects.filter(
        Q(title__icontains = search_term) | Q(description__icontains = search_term),).order_by('-id')
    
    context = {'page_title': f'Pesquisa por "{search_term}" |',
               'search_term': search_term,
               'receitas': receitas,}
    return render(request, 'receitas/pages/search.html', context)