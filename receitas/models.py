from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    class meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name
    



class Receita(models.Model):
    class meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'

    title = models.CharField(verbose_name='Titulo' , max_length=65)
    description = models.CharField(verbose_name='Descrição' ,max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(verbose_name="Tempo de Preparação")
    preparation_time_unit = models.CharField(verbose_name="Unidade", max_length=65)
    servings = models.IntegerField(verbose_name="Porções")
    servings_unit = models.CharField(verbose_name="Unidade da Porção", max_length=65)
    preparation_steps = models.TextField(verbose_name="Etapas da preparação")
    preparation_steps_is_html = models.BooleanField(verbose_name="É um html", default=False)
    created_at = models.DateTimeField(verbose_name="Criado em", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Atualizado em", auto_now=True)
    is_published = models.BooleanField(verbose_name="Está publicado", default=False)
    cover = models.ImageField(verbose_name="Apresentação", upload_to='receitas/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
         return reverse('receitas:receita', args=(self.id,))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)