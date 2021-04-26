import os
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from fby_market.settings import MEDIA_ROOT, MEDIA_URL, DEBUG, YaMarket


def get_path(instance, filename):
    return f'{instance.username}/image.{filename.split(".")[-1]}'


class User(AbstractUser):
    image = models.ImageField(verbose_name='аватарка', upload_to=get_path, default=f'base/base.png', blank=True)
    client_id = models.CharField(verbose_name='Client ID', max_length=255, default='')
    token = models.CharField(verbose_name='YM token', max_length=255, default='')
    shop_id = models.CharField(verbose_name='Shop ID', max_length=255, default='')


    @property
    def get_image(self):
        return f'{MEDIA_URL}/{self.image}'

    def clean(self):
        if self.image and self.client_id and self.token and self.shop_id:
            return True
        if not self.image or not os.path.exists((MEDIA_ROOT + '/' + str(self.image)).replace('\\', '/')):
            self.image = f'base/base.png'
        if not (self.client_id and self.token and self.shop_id):
            raise ValidationError('Введите все данные')

    @staticmethod
    def debug_mod_keys():
        return True if DEBUG else False

    def get_client_id(self):
        return YaMarket.CLIENT_ID if self.debug_mod_keys() else self.client_id

    def get_token(self):
        return YaMarket.TOKEN if self.debug_mod_keys() else self.token

    def get_shop_id(self):
        return YaMarket.SHOP_ID if self.debug_mod_keys() else self.shop_id
