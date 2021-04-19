from django.contrib.auth.models import AbstractUser
from django.db import models


def get_path(instance, filename):
    return f'user_{instance.id}/image.{filename.split(".")[-1]}'


class User(AbstractUser):
    image = models.ImageField(verbose_name='аватарка', upload_to=get_path, default=f'base/base.png', blank=True)

