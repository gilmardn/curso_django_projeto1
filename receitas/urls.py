from django.urls import path
from receitas.views import home, receitas, category


urlpatterns = [
    path('', home, name='receitas-home'),
    path('receitas/category/<int:category_id>/', category, name='receitas-category'),
    path('receitas/<int:id>/', receitas, name='receitas-receita'),
  
]