from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(verbose_name='аватарка', upload_to='', default=f'base/base.png', blank=True)

