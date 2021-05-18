import os
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from fby_market.settings import MEDIA_URL, DEBUG, YaMarket


def get_path(instance, filename):
    """Метод для получения пути сохранения аватарки пользователя"""
    return f'{instance.username}/image.{filename.split(".")[-1]}'


class User(AbstractUser):
    image = models.ImageField(verbose_name='Аватарка', upload_to=get_path, default=f'base/base.png', blank=True)
    client_id = models.CharField(verbose_name='Client ID', max_length=255, default='', blank=True)
    token = models.CharField(verbose_name='YM token', max_length=255, default='', blank=True)
    shop_id = models.CharField(verbose_name='Shop ID', max_length=255, default='', blank=True)
    verified = models.BooleanField(default=False)

    @property
    def get_image(self):
        """Метод для получения пути хранения картинки пользователя"""
        return f'{MEDIA_URL}/{self.image}'

    def clean(self):
        data = {self.client_id, self.token, self.shop_id}
        if len(data) == 1:
            if '' not in data:
                raise ValidationError('Все ключи одинаковые')
        elif len(data) < 3 or (len(data) == 3 and '' in data):
            raise ValidationError('Введите все 3 ключа')
        if not self.image and not os.path.exists(self.get_image.replace('\\', '/')):
            self.image = f'base/base.png'

        if self.email != '':
            if User.objects.filter(email=self.email):
                raise ValidationError('Данная почта уже зарегистрирована')

    @staticmethod
    def __debug_mod(db, sett):
        """Метод для получения необходимых данных, в зависимости от наличия DEBUG режима"""
        if DEBUG:
            return sett
        return db

    def get_client_id(self):
        """Метод для получения client id в зависимости от DEBUG режима"""
        return self.__debug_mod(db=self.client_id, sett=YaMarket.CLIENT_ID)

    def get_token(self):
        """Метод для получения token в зависимости от DEBUG режима"""
        return self.__debug_mod(db=self.token, sett=YaMarket.TOKEN)

    def get_shop_id(self):
        """Метод для получения shop id в зависимости от DEBUG режима"""
        return self.__debug_mod(db=self.shop_id, sett=YaMarket.SHOP_ID)
