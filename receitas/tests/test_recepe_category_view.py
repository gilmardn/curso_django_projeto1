from django.urls import resolve, reverse
from receitas import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewsTest(RecipeTestBase):
    def testa_recipe_category_view_funcao_correta(self):
        view = resolve(
            reverse('receitas-category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)

    def testa_recipe_category_view_returns_404_se_nao_encontar_receita(self):
        response = self.client.get(
            reverse('receitas-category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def testa_recipe_category_carrega_modelo_receita(self):
        needed_title = 'This is a category test'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('receitas-category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def testa_recipe_category_nao_carrega_receitas_nao_publicadas(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('receitas-receita', kwargs={'id': recipe.category.id})
        )

        self.assertEqual(response.status_code, 404)
