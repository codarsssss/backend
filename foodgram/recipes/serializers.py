from rest_framework.serializers import ModelSerializer

from recipes.models import Tag as Tag, Ingredient


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id', 'name', 'color', 'slug'
        read_only_fields = 'id', 'name', 'color', 'slug'


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = 'id', 'name', 'measurement_unit'
        read_only_fields = 'id', 'name', 'measurement_unit'
