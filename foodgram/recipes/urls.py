from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagsViewSet

router = DefaultRouter()
# router.register('recipes', RecipeViewSet)
# router.register('ingredients', IngredientViewSet)
router.register('tags', TagsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
