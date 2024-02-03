from rest_framework.serializers import ModelSerializer

from recipes.models import Tag as Tag


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id', 'name', 'color', 'slug'
        read_only_fields = 'id', 'name', 'color', 'slug'
