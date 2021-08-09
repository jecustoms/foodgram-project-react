from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ..users.serializers import UserSerializer
from . import models
from .custom_field import Base64ImageField

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientWriteSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()

    class Meta:
        model = models.Ingredient
        fields = ('id', 'amount')


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = models.RecipeIngredient
        fields = ('id', 'name', 'amount', 'measurement_unit')
        read_only_fields = ('amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(source='amounts', many=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = models.Recipe
        fields = ('id', 'author', 'name', 'text', 'image',
                  'ingredients', 'tags', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.is_favorited.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.is_in_shopping_cart.filter(user=user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=models.Tag.objects.all(), many=True
    )

    class Meta:
        model = models.Recipe
        fields = ('id', 'author', 'name', 'text', 'image',
                  'ingredients', 'tags', 'cooking_time')

    def validate_ingredients(self, data):
        ingredients_set = set()
        for item in data:
            amount = item.get('amount')
            if int(amount) < 0:
                raise serializers.ValidationError(
                    'Количество должно быть >= 0'
                )
            ingredient_id = item.get('id')
            if ingredient_id in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в рецепте не должен повторяться.')
            ingredients_set.add(id)
        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = models.Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            ingredient_id = ingredient['id']
            models.RecipeIngredient.objects.create(
                ingredient=get_object_or_404(models.Ingredient,
                                             id=ingredient_id),
                recipe=recipe, amount=amount
            )
        for tag in tags_data:
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        models.RecipeIngredient.objects.filter(recipe=instance).delete()
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            ingredient_id = ingredient['id']
            models.RecipeIngredient.objects.create(
                ingredient=get_object_or_404(models.Ingredient,
                                             id=ingredient_id),
                recipe=instance, amount=amount
            )
        for tag in tags_data:
            instance.tags.add(tag)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
        return data


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Favourite
        fields = ('user', 'recipe')

    def validate(self, data):
        if request.method == 'GET':
            if not data['user'].is_favorited.filter(
                recipe=data['recipe']
            ).exists():
                models.Favourite.objects.create(
                    user=data['user'], recipe=data['recipe']
                )
                return data
            raise serializers.ValidationError(
                'Этот рецепт уже есть в избранном'
            )
        if not data['user'].is_favorited.filter(
            recipe=data['recipe']
        ).exists():
            raise serializers.ValidationError(
                'Этого рецепта не было в вашем избранном'
            )


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data):
        if request.method == 'GET':
            if not data['user'].is_in_shopping_cart.filter(
                recipe=data['recipe']
            ).exists():
                models.ShoppingCart.objects.create(
                    user=data['user'], recipe=data['recipe']
                )
                return data
            raise serializers.ValidationError(
                'Этот рецепт уже есть в списке покупок'
            )
        if not data['user'].is_in_shopping_cart.filter(
            recipe=data['recipe']
        ).exists():
            raise serializers.ValidationError(
                'Этого рецепта не было в вашем списке покупок'
            )
