from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', TokenCreateView.as_view(), name='token_obtain'),
    path(
        'auth/token/logout/',
        TokenDestroyView.as_view(),
        name='token_destroy'
    ),
]
