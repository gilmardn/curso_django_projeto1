from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from authors.forms import RegisterForm


def register_view(request):

    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)
    context =  {'form': form, 'form_action': reverse('authors:create'),}
    return render(request, 'authors/pages/register_view.html', context)


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

    return redirect('authors:register')