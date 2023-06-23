from django.urls import resolve, reverse

from recipes import views

from .test_recipeBase import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    # RECIPE DETAIL TESTS

    def test_recipe_recipe_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={
            'id': 1
        }))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_status_code_404(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={
            'id': 1000
        }))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_not_load_not_published(self):
        """
            Test if recipe is_published = false dont show
        """
        recipe = self.makeRecipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs={
            'id': recipe.id,
        }))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_loads_recipes(self):
        recipe = self.makeRecipe(title='This is a detail test')

        response = self.client.get(reverse('recipes:recipe', args=((1,))))
        response_context = response.context
        recipes = response_context['recipe']
        content = response.content.decode('utf-8')

        self.assertEqual(recipes.title, recipe.title)

        self.assertIn(recipe.title, content)
        self.assertIn(recipe.description, content)
        self.assertIn(str(recipe.preparation_time) + ' ' +
                      recipe.preparation_time_unit, content)
        self.assertIn(str(recipe.servings) + ' ' +
                      recipe.servings_unit, content)
        self.assertIn(recipe.author.first_name, content)
        self.assertIn(recipe.category.name, content)
