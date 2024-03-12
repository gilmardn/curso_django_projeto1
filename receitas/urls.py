from django.urls import path
from receitas.views import home, receitas, category, search
from receitas.views import RecipeListViewCategory, RecipeListViewSearch, RecipeListViewHome, RecipeDetail

#app_name = 'receitas'

urlpatterns = [
    #path('', home, name='receitas-home'),
    path('', RecipeListViewHome.as_view(), name='receitas-home'),  
    #path('receitas/search/', search, name='receitas-search'),
    path('receitas/search/', RecipeListViewSearch.as_view(), name='receitas-search'),
    #path('receitas/category/<int:category_id>/', category, name='receitas-category'),
    path('receitas/category/<int:category_id>/', RecipeListViewCategory.as_view(), name='receitas-category'),
    #path('receitas/<int:id>/', receitas, name='receitas-receita'),
    path('receitas/<int:pk>/', RecipeDetail.as_view(), name='receitas-receita'),
    
  
]