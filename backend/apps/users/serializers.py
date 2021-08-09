from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..api.models import Recipe, Subscription

User = get_user_model()


class SubRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        model = User
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.subscriber.filter(user=user).exists()

    def validate(self, data):
        if requeset.method == 'GET':
            if data['author'] != data['user'] and not data['subscribed']:
                Subscription.objects.create(
                    user=data['user'], author=data['author']
                )
                return data
            raise serializers.ValidationError(
                'Вы или уже подписаны на этого автора, или пытаетесь '
                'подписаться на себя, что невозможно'
            )
        if not data['user'].subscribed_on.filter(
            author=data['author']
        ).exists():
            raise serializers.ValidationError(
                'Вы не подписаны на данного автора (напоминание: на себя '
                'подписаться невозможно)'
            )


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        model = User

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.subscriber.filter(user=user).exists()

    def get_recipes(self, obj):
        request = self.context['request']
        limit = int(request.query_params.get('recipes_limit', 3))
        recipes = obj.recipes.all()[:limit]
        serializer = SubRecipeSerializer(
            recipes, many=True, context={'request': request}
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()
