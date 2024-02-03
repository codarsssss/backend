from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import Tag, Ingredient
from recipes.serializers import TagsSerializer, IngredientsSerializer


class TagsViewSet(ReadOnlyModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()


class IngredientsViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self): # можно на бекенд потом сделать
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__startswith=name)
        return queryset

