from django.urls import resolve, reverse

from recipes import views

from .test_recipeBase import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    # HOME TESTS

    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_no_recipes_found(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            "<h1>No recipes found!!</h1>",
            response.content.decode('utf-8')
        )

    def test_recipe_home_loads_recipes(self):
        recipe = self.makeRecipe()

        response = self.client.get(reverse('recipes:home'))
        response_context = response.context
        recipes = response_context['recipes']
        content = response.content.decode('utf-8')

        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes.first().title, recipe.title)

        self.assertIn(recipe.title, content)
        self.assertIn(recipe.description, content)
        self.assertIn(str(recipe.preparation_time) + ' ' +
                      recipe.preparation_time_unit, content)
        self.assertIn(str(recipe.servings) + ' ' +
                      recipe.servings_unit, content)
        self.assertIn(recipe.author.first_name, content)
        self.assertIn(recipe.category.name, content)

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
