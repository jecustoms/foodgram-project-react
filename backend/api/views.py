from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientSearchFilter, TagAndAuthorFilter
from .mixins import BaseTagAndIngredientViewSet
from .models import (Cart, Favorite, Ingredient, IngredientAmount, Recipe,
                     Subscribe, Tag, User)
from .paginations import LimitPageNumberPagination
from .permissions import IsAuthorOrReadOnly, IsStaffOrReadOnly
from .serializers import (IngredientSerializer, RecipeMinifiedSerializer,
                          RecipeSerializer, SubscribeSerializer, TagSerializer,
                          UserSerializer)


class TagsViewSet(BaseTagAndIngredientViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(BaseTagAndIngredientViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_class = TagAndAuthorFilter
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )
        return serializer

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Recipe.objects.all()

        queryset = Recipe.objects.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user=user, recipe_id=OuterRef('pk')
                )
            ),
            is_in_shopping_cart=Exists(
                Cart.objects.filter(
                    user=user, recipe_id=OuterRef('pk')
                )
            )
        )

        if self.request.GET.get('is_favorited'):
            return queryset.filter(is_favorited=True)
        elif self.request.GET.get('is_in_shopping_cart'):
            return queryset.filter(is_in_shopping_cart=True)

        return queryset

    @action(detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user

        return self.add_obj(Favorite, user, recipe)

    @favorite.mapping.delete
    def del_favorite(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        return self.delete_obj(Favorite, user, recipe)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        return self.add_obj(Cart, user, recipe)

    @shopping_cart.mapping.delete
    def del_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        return self.delete_obj(Cart, user, recipe)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        final_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__in_cart__user=user
        )
        for ingredient_item in ingredients:
            name = ingredient_item.ingredient.name
            measurement_unit = ingredient_item.ingredient.measurement_unit
            amount = ingredient_item.amount
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                final_list[name]['amount'] += amount

        pdfmetrics.registerFont(TTFont('FiraSans', 'FiraSans.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('FiraSans', size=16)
        page.drawString(200, 800, 'Список ингредиентов')
        height = 750
        i = 1

        for name, data in final_list.items():
            page.drawString(
                50,
                height,
                (f'{i}) { name } - {data["amount"]}, '
                 f'{data["measurement_unit"]}')
            )
            height -= 25
            i += 1
        page.showPage()
        page.save()
        Cart.objects.filter(user=user).delete()

        return response

    def add_obj(self, model, user, recipe):
        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response({
                'errors': 'Рецепт уже добавлен в список'
            }, status=status.HTTP_400_BAD_REQUEST)

        obj = model.objects.create(
            user=user, recipe=recipe
        )
        obj.save()
        serializer = RecipeMinifiedSerializer(recipe)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, recipe):
        obj = model.objects.filter(user=user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = UserSerializer

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        subscriber = get_object_or_404(User, id=id)

        if (Subscribe.objects.filter(user=user, subscriber=subscriber)
                .exists() or user == subscriber):
            return Response({
                'errors': ('Вы уже подписаны на этого пользователя '
                           'или подписываетесь на самого себя')
            }, status=status.HTTP_400_BAD_REQUEST)

        subscribe = Subscribe.objects.create(user=user, subscriber=subscriber)
        subscribe.save()
        serializer = SubscribeSerializer(
            subscribe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        user = request.user
        subscriber = get_object_or_404(User, id=id)
        subscribe = Subscribe.objects.filter(
            user=user, subscriber=subscriber
        )
        if subscribe.exists():
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
