from random import choice, randint

from django.contrib.auth.models import User
from django.utils.text import slugify
from faker import Faker

from recipes.models import Category, Recipe

# Criação de uma instância do Faker para dados fictícios
fake = Faker()

# Lista de unidades de tempo para o campo "preparation_time_unit"
time_units = ['minutes', 'hours', 'days']

# Lista de unidades de medida para o campo "servings_unit"
serving_units = ['slices', 'pieces', 'cups']

# Lista de categorias existentes (se você tiver categorias já definidas)
categories = Category.objects.all()

# Lista de usuários existentes (se você tiver usuários já definidos)
users = User.objects.all()

# Loop para criar 10 objetos aleatórios do modelo Recipe
for _ in range(10):
    title = fake.words(nb=3)  # Gera uma lista de 3 palavras fictícias para o título
    description = fake.text(max_nb_chars=100)  # Gera uma descrição fictícia
    slug = slugify(" ".join(title))  # Cria um slug baseado no título
    preparation_time = randint(10, 60)  # Gera um tempo de preparo aleatório entre 10 e 60 minutos
    preparation_time_unit = choice(time_units)  # Seleciona uma unidade de tempo aleatória
    servings = randint(1, 6)  # Gera um número de porções aleatório entre 1 e 6
    servings_unit = choice(serving_units)  # Seleciona uma unidade de medida aleatória
    preparation_steps = fake.paragraphs(nb=3, ext_word_list=None)  # Gera 3 parágrafos fictícios para os passos de preparo
    preparation_steps_is_html = False  # Define se os passos de preparo contêm HTML (definido como False neste exemplo)
    is_published = choice([True, False])  # Define se a receita está publicada ou não de forma aleatória
    cover = ''  # Deixe em branco para este exemplo
    category = choice(categories) if categories else None  # Seleciona uma categoria aleatória ou None se não houver categorias
    author = choice(users) if users else None  # Seleciona um autor aleatório ou None se não houver usuários

    recipe = Recipe.objects.create(
        title=" ".join(title),
        description=description,
        slug=slug,
        preparation_time=preparation_time,
        preparation_time_unit=preparation_time_unit,
        servings=servings,
        servings_unit=servings_unit,
        preparation_steps="\n\n".join(preparation_steps),
        preparation_steps_is_html=preparation_steps_is_html,
        is_published=is_published,
        cover=cover,
        category=category,
        author=author
    )
    print(f"Recipe created: {recipe.title}")