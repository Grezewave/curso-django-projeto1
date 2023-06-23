from django.urls import resolve, reverse

from recipes import views

from .test_recipeBase import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

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
