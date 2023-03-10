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

    def test_recipe_home_template_not_load_not_published(self):
        """
            Test if recipe is_published = false dont show
        """
        self.makeRecipe(is_published=False)

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

    # RECIPE SEARCH TEST

    def test_recipe_search_view_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_recipe_search_loads_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_on_page_title_scaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertIn('Search for &quot;teste&quot;',
                      response.content.decode('utf-8'))
