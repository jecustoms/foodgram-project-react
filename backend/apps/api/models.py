from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from .fields import fields

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        unique=True,
        max_length=24
    )
    color = fields.ColorField(
        verbose_name='Цвет',
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
    )

    class Meta:
        app_label = 'api'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        blank=False,
        max_length=50
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=10,
        blank=False
    )

    class Meta:
        app_label = 'api'
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='subscribed_on')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='subscriber')

    class Meta:
        app_label = 'api'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='subscribe'
            )
        ]

    def __str__(self):
        return (f'Подписка {self.user.username} на {self.author.username}')


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    name = models.CharField(
        verbose_name='Название',
        max_length=30,
        blank=False
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
        blank=False,
    )
    text = models.TextField(
        verbose_name='Описание',
        blank=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        blank=False,
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        to=Tag,
        blank=False,
        related_name='recipes',
        verbose_name='Тэги'
    )
    cooking_time = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(
                1, message='минимальное время готовки 1 минута'
            )
        ],
        blank=False,
        verbose_name='Время приготовления в минутах'
    )

    class Meta:
        app_label = 'api'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amounts'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amounts'
    )
    amount = models.PositiveIntegerField()

    class Meta:
        app_label = 'api'
        verbose_name = 'Ингредиент-рецепт'
        verbose_name_plural = 'Ингредиент-рецепт'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_unique'
            )
        ]

    def __str__(self):
        return f'Количество {self.ingredient} в рецепте {self.recipe}'


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_favorited'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited'
    )

    class Meta:
        app_label = 'api'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='user_recept_unique'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart'
    )

    class Meta:
        app_label = 'api'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='cart_user_recept_unique'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок {self.user}'
