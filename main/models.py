import os
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from fby_market.settings import MEDIA_ROOT, MEDIA_URL, DEBUG, YaMarket


def get_path(instance, filename):
    return f'{instance.username}/image.{filename.split(".")[-1]}'


class User(AbstractUser):
    image = models.ImageField(verbose_name='Аватарка', upload_to=get_path, default=f'base/base.png', blank=True)
    client_id = models.CharField(verbose_name='Client ID', max_length=255, default='', blank=True)
    token = models.CharField(verbose_name='YM token', max_length=255, default='', blank=True)
    shop_id = models.CharField(verbose_name='Shop ID', max_length=255, default='', blank=True)

    @property
    def get_image(self):
        return f'{MEDIA_URL}/{self.image}'

    def clean(self):
        data = {self.client_id, self.token, self.shop_id}
        if len(data) == 1:
            if '' not in data:
                raise ValidationError('Все ключи одинаковые')
        elif len(data) < 3 or (len(data) == 3 and '' in data):
            raise ValidationError('Введите все 3 ключа')
        if not self.image or not os.path.exists(f'{MEDIA_ROOT}/{self.image}'.replace('\\', '/')):
            self.image = f'base/base.png'

    @staticmethod
    def __debug_mod(db, sett):
        if DEBUG:
            return sett
        return db

    def get_client_id(self):
        return self.__debug_mod(db=self.client_id, sett=YaMarket.CLIENT_ID)

    def get_token(self):
        return self.__debug_mod(db=self.token, sett=YaMarket.TOKEN)

    def get_shop_id(self):
        return self.__debug_mod(db=self.shop_id, sett=YaMarket.SHOP_ID)
