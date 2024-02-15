from django.contrib import admin

from receitas.models import Category, Receita

# Registrar assim.
@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    ...

# ou assim
class CategoryAdmin(admin.ModelAdmin):
    ...

admin.site.register(Category, CategoryAdmin)
