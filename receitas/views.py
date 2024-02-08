from django.shortcuts import render


def home(request):
    context = {'name': 'Gilmar Dalla Nora'}
    return render(request, 'receitas/pages/home.html', context)
