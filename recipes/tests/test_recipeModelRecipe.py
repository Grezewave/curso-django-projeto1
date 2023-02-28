from django.core.exceptions import ValidationError
from parameterized import parameterized

from recipes.models import Recipe
from recipes.tests.test_recipeBase import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.makeRecipe()
        return super().setUp()

    def makeRecipeNoDefaults(self):
        recipe = Recipe(
            category=self.makeCategory(name='Test Default Category'),
            author=self.makeAuthor(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )

        recipe.full_clean()
        recipe.save()

        return recipe

    def test_recipe_title_raises_error_in_more_65_chars(self):
        self.recipe.title = 'Titulo com mais de 65 caracteres'*3

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # Valida as inputs apenas aqui

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 20),
        ('servings_unit', 20),
    ])
    def test_recipe_fields_max_length(self, field, length):
        setattr(self.recipe, field, 'V'*(length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # Valida as inputs apenas aqui

    def test_recipe_steps_html_false_default(self):
        recipe = self.makeRecipeNoDefaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='Recipe html is not FALSE!!!')

    def test_recipe_published_false_default(self):
        recipe = self.makeRecipeNoDefaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='Recipe published is not FALSE!!!')

    def test_recipe_str_representation(self):
        self.recipe.title = 'Testing representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), self.recipe.title)
