from django.urls import path
from authors.views import register_view, register_create, login_create, \
                    login_view, logout_view, dashboard, dashboard_receita_edit, \
                    dashboard_receita_new, dashboard_receita_delete

from authors.views_class import DashboardReceita, DashboardReceitaDelete


app_name = 'authors'

urlpatterns = [
    path('register/', register_view, name= 'register'),
    path('register/create/', register_create, name= 'register_create'),
    path('login/', login_view, name= 'login'),
    path('login/create/', login_create, name= 'login_create'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    #path('dashboard/recipe/new/', dashboard_receita_new, name='dashboard_receita_new'),
    path('dashboard/recipe/new/', DashboardReceita.as_view(), name='dashboard_receita_new'),
    #path('dashboard/receita/delete/', dashboard_receita_delete, name='dashboard_receita_delete'),
    path('dashboard/receita/delete/', DashboardReceitaDelete.as_view(), name='dashboard_receita_delete'),
    #path('dashboard/receita/<int:id>/edit/', dashboard_receita_edit, name='dashboard_receita_edit'),
    path('dashboard/receita/<int:id>/edit/', DashboardReceita.as_view(), name='dashboard_receita_edit'),
]
