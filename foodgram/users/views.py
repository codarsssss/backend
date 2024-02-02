from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, \
    HTTP_400_BAD_REQUEST

from .pagenation import UserPaginator
from .serializers import UserSerializer1, SubscribeSerializer
from .models import Subscribe


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer1
    pagination_class = UserPaginator
    permission_classes = [IsAuthenticated]

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk=None):
        # Получаем пользователя, на которого подписываемся (автора).
        author = get_object_or_404(User, id=pk)
        # Получаем текущего пользователя (подписчика).
        user = request.user

        # Проверяем, что пользователь не пытается подписаться на самого себя.
        if user == author:
            return Response({'errors': 'Нельзя подписаться на себя'},
                            status=HTTP_400_BAD_REQUEST)

        # Если метод запроса - POST, то это запрос на подписку.
        if request.method == 'POST':
            # Пытаемся получить объект подписки, если он уже существует.
            subscribe, created = Subscribe.objects.get_or_create(user=user,
                                                                 author=author)

            # Если подписка уже существует, возвращаем ошибку.
            if not created:
                return Response({'errors': 'Подписка уже оформлена'},
                                status=HTTP_400_BAD_REQUEST)

            # Если подписка успешно создана, возвращаем данные подписки и статус 201 (Created).
            serializer = SubscribeSerializer(subscribe,
                                             context={'request': request})
            return Response(serializer.data, status=HTTP_201_CREATED)

        # Если метод запроса - DELETE, то это запрос на отмену подписки.
        elif request.method == 'DELETE':
            try:
                # Пытаемся найти объект подписки для текущего пользователя и автора.
                subscription = Subscribe.objects.get(user=user, author=author)
                # Если подписка найдена, удаляем ее.
                subscription.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            except Subscribe.DoesNotExist:
                # Если подписка не найдена, возвращаем ошибку.
                return Response({'errors': 'Подписка не найдена'},
                                status=HTTP_400_BAD_REQUEST)

        # if request.method == 'DELETE':
        #     Subscribe.objects.filter(user=user, author=author).delete()
        #     return Response(status=HTTP_204_NO_CONTENT)
        # return Response({
        #     'errors': 'Вы не были подписаны на этого автора рецептов'
        # }, status=HTTP_400_BAD_REQUEST)

    # def create(self, validated_data: dict) -> User:
    #     serializer = UserSerializer(data=validated_data)
    #     serializer.is_valid(
    #         raise_exception=True)  # Это вызывает ValidationError, если данные не проходят валидацию
    #     return serializer.save()
