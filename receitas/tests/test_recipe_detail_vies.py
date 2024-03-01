from django.urls import resolve, reverse
from receitas import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewsTest(RecipeTestBase):

    def testa_recipe_detail_view_e_funcao_correta(self):
        view = resolve(
            reverse('receitas-receita', kwargs={'id': 2})
        )
        self.assertIs(view.func, views.receitas)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('receitas-receita', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'

        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse(
                'receitas-receita',
                kwargs={
                    'id': 1
                }
            )
        )
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'receitas-receita',
                kwargs={
                    'id': recipe.id
                }
            )
        )

        self.assertEqual(response.status_code, 404)


