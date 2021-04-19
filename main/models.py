import os

from django.contrib.auth.models import AbstractUser
from django.db import models

from fby_market.settings import MEDIA_ROOT


def get_path(instance, filename):
    return f'{instance.username}/image.{filename.split(".")[-1]}'


class User(AbstractUser):
    image = models.ImageField(verbose_name='аватарка', upload_to=get_path, default=f'base/base.png', blank=True)

    def check_image(self):
        if not self.image or not os.path.exists((MEDIA_ROOT + '/' + str(self.image)).replace('\\', '/')):
            self.image = f'base/base.png'
