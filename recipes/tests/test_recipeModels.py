from recipes.tests.test_recipeBase import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.makeRecipe()
        return super().setUp()
