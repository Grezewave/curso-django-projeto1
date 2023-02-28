from django.core.exceptions import ValidationError

from recipes.tests.test_recipeBase import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.makeCategory(
            name='Category Testing'
        )
        return super().setUp()

    def test_recipe_category_model_string_representarion_is_name_field(self):
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
