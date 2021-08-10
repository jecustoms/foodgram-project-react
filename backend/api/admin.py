from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Cart, Favorite, Ingredient, Recipe, Subscribe, Tag, User


class IngredientAmountInline(admin.TabularInline):
    model = Ingredient.recipes.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = ['measurement_unit']
    search_fields = ['name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'in_favorites']
    list_filter = ['author', 'tags']
    search_fields = ['name']
    inlines = [IngredientAmountInline]

    def in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']
    list_filter = ['user']
    search_fields = ['user__username', 'recipe__name']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscriber']


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'is_staff']
    list_filter = ['is_staff']
