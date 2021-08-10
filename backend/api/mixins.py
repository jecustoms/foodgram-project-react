from rest_framework import mixins, viewsets

from .permissions import IsStaffOrReadOnly


class BaseTagAndIngredientViewSet(mixins.ListModelMixinx,
                                  mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    permission_classes = [IsStaffOrReadOnly]
