from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import Tag
from recipes.serializers import TagsSerializer


class TagsViewSet(ReadOnlyModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()

