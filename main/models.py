import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from fby_market.settings import MEDIA_ROOT, MEDIA_URL


def get_path(instance, filename):
    return f'{instance.username}/image.{filename.split(".")[-1]}'


class User(AbstractUser):
    image = models.ImageField(verbose_name='аватарка', upload_to=get_path, default=f'base/base.png', blank=True)

    @property
    def get_image(self):
        return f'{MEDIA_URL}/{self.image}'

    def clean(self):
        if self.image:
            return True
        if not self.image or not os.path.exists((MEDIA_ROOT + '/' + str(self.image)).replace('\\', '/')):
            self.image = f'base/base.png'
