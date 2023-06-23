from django.urls import resolve, reverse

from recipes import views

from .test_recipeBase import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    # CATEGORY TESTS

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={
            'category_id': 1000
        }))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_status_code_404(self):
        response = self.client.get(reverse('recipes:category', kwargs={
            'category_id': 1000
        }))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_not_load_not_published(self):
        """
            Test if recipe is_published = false dont show
        """
        recipe = self.makeRecipe(is_published=False)

        response = self.client.get(reverse('recipes:category', kwargs={
            'category_id': recipe.category.id,
        }))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_loads_recipes(self):
        recipe = self.makeRecipe(title='This is a category test')

        response = self.client.get(reverse('recipes:category', args=((1,))))
        response_context = response.context
        recipes = response_context['recipes']
        content = response.content.decode('utf-8')

        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0].title, recipe.title)

        self.assertIn(recipe.title, content)
        self.assertIn(recipe.description, content)
        self.assertIn(str(recipe.preparation_time) + ' ' +
                      recipe.preparation_time_unit, content)
        self.assertIn(str(recipe.servings) + ' ' +
                      recipe.servings_unit, content)
        self.assertIn(recipe.author.first_name, content)
        self.assertIn(recipe.category.name, content)