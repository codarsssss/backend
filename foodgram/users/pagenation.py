from rest_framework.pagination import LimitOffsetPagination


class UserPaginator(LimitOffsetPagination):
    default_limit = 6
