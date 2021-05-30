from django.db import models


class Feedback(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Имя', null=True
    )
    email = models.CharField(
        max_length=255,
        verbose_name='E-mail для связи', null=True
    )
    message = models.TextField(
        verbose_name='Текст',
        null=True,
        blank=True
    )
