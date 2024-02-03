from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField('Название', unique=True, max_length=200)
    color = models.CharField(
        'HEX-код', max_length=7,
        validators=[RegexValidator(regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                                   message='Ошибка ввода HEX!!!')])
    slug = models.SlugField('Слаг', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
