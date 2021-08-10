from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


class Ingredient(models.Model):

    name = models.CharField(
        'Название',
        max_length=100
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=10
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    BLUE = '#4A61DD'
    ORANGE = '#E26C2D'
    GREEN = '#49B64E'
    PURPLE = '#8775D2'
    YELLOW = '#F9A62B'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
    ]

    name = models.CharField(
        'Название',
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
    )
    color = models.CharField(
        'Цветовой код',
        max_length=7,
        choices=COLOR_CHOICES,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Subscribe(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Подписчик',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscriber'],
                name='unique subscribe',
            )
        ]


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    name = models.CharField(
        'Название',
        max_length=100
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Текстовое описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингридиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[ 
            validators.MinValueValidator( 
                1,
                message='Минимальное время приготовления 1 минута' 
            ) 
        ],
        verbose_name='Время приготовления',

    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
    )

    class Meta:
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='in_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
