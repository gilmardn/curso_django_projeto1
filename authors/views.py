from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from receitas.models import Receita
from authors.forms.login import LoginForm
from authors.forms.register_form import RegisterForm
from authors.forms.receita_form import AuthorReceitaForm

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    context =  {'form': form, 'form_action': reverse('authors:register_create'),}
    return render(request, 'authors/pages/register_view.html', context)
#===============================================================================================

def register_create(request):
    if not request.POST:
        raise Http404()
    POSTAR = request.POST
    request.session['register_form_data'] = POSTAR
    form = RegisterForm(POSTAR)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user = form.save(commit=True)
        messages.success(request, 'Your user is create, please log in.')
        del(request.session['register_form_data'])

        return redirect(reverse('authors:login'))

    return redirect('authors:register')
#===============================================================================================

def login_view(request):
    form = LoginForm()
    context =  {'form': form, 'form_action': reverse('authors:login_create'),}
    return render (request, 'authors/pages/login.html', context)
#===============================================================================================

def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')

    else:
        messages.error(request, 'Invalid username or password')

    return redirect(reverse('authors:dashboard'))
#===============================================================================================

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))
    
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))
    
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect(reverse('authors:login'))
#===============================================================================================   

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    receitas = Receita.objects.filter(
        is_published=False,
        author=request.user
    )

    context={'receitas': receitas,}
    return render(request, 'authors/pages/dashboard.html', context)
#===============================================================================================

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_receita_edit(request, id):
    receita = Receita.objects.filter(is_published=False, author=request.user, pk=id,).first()

    if not receita:
        raise Http404()
    
    form = AuthorReceitaForm(
        request.POST or None , 
        files=request.FILES or None,
        instance=receita)

    if form.is_valid():
        receita = form.save(commit=False)

        receita.author = request.user
        receita.preparation_steps_is_html = False
        receita.is_published = False

        receita.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        return redirect(reverse('authors:dashboard_receita_edit', args=(id,)))

    context = {'form': form}
    return render(request, 'authors/pages/dashboard_receita.html', context)
#===============================================================================================












@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_receita_new(request):
    form = AuthorReceitaForm(
        data=request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        receita: Receita = form.save(commit=False)

        receita.author = request.user
        receita.preparation_steps_is_html = False
        receita.is_published = False

        receita.save()

        messages.success(request, 'Salvo com sucesso!')
        return redirect(
            reverse('authors:dashboard_recipe_edit', args=(receita.id,))
        )
    
    context={'form': form, 'form_action': reverse('authors:dashboard_recipe_new')}

    return render(request, 'authors/pages/dashboard_recipe.html', context)
#===============================================================================================







@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_receita_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    receita = Receita.objects.filter(is_published=False, \
        author=request.user, pk=id,).first()

    if not receita:
        raise Http404()

    receita.delete()
    messages.success(request, 'Deleted successfully.')
    return redirect(reverse('authors:dashboard'))