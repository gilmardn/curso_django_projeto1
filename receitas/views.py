from django.shortcuts import render
from utils.receitas.factory import make_receita
from receitas.models import  Receita

def home(request):
    receitas = Receita.objects.filter(is_published=True).order_by('-id')
    #context = {'receitas':make_receita() for _ in range(10)}
    context = {'receitas':receitas}
    return render(request, 'receitas/pages/home.html', context)

def category(request, category_id):
    receitas = Receita.objects.filter(category__id=category_id, is_published=True).order_by('-id')
    # context = {'receitas':make_receita() for _ in range(10)}
    context = {'receitas':receitas}
    return render(request, 'receitas/pages/category.html', context)


def receitas(request, id):
    context = {'receita': make_receita(), 'is_detail_page': True}
    return render(request, 'receitas/pages/receita_view.html', context)
