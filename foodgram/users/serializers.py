from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

from .models import Subscribe

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'allow_blank': False, 'required': True},
            'last_name': {'allow_blank': False, 'required': True},
            'password': {'write_only': True}
        }

class SubscribeSerializer(ModelSerializer):
    class Meta:
        model = Subscribe
        fields = 'user', 'author'


class ExtendUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=request.user,
                                     author=obj).exists()


# class UserRegistrationSerializer(UserCreateSerializer):
#     class Meta(UserCreateSerializer.Meta):
#         fields = (
#             'email',
#             'username',
#             'first_name',
#             'last_name',
#             'password',
#         )
#
#
# class UserDetailSerializer(UserSerializer):
#     is_subscribed = serializers.SerializerMethodField()
#
#     class Meta(UserSerializer.Meta):
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed'
#         )
#
#     def get_is_subscribed(self, obj):
#         request = self.context.get('request')
#         if request is None or request.user.is_anonymous:
#             return False
#         return Follow.objects.filter(
#             user=request.user,
#             author=obj).exists()
#
#
# class AuthTokenSerializer(serializers.Serializer):
#     email = serializers.EmailField(label='Email')
#     password = serializers.CharField(
#         label=('Password',),
#         style={'input_type': 'password'},
#         trim_whitespace=False
#     )
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         if email and password:
#             user = authenticate(
#                 request=self.context.get('request'),
#                 email=email,
#                 password=password
#             )
#             if not user:
#                 msg = 'Неверные учетные данные.'
#                 raise serializers.ValidationError(
#                     msg,
#                     code='authorization')
#         else:
#             msg = 'Запрос должен содержать email и пароль.'
#             raise serializers.ValidationError(
#                 msg,
#                 code='authorization')
#
#         attrs['user'] = user
#         return attrs