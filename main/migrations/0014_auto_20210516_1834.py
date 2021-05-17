# Generated by Django 3.1.7 on 2021-05-16 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20210516_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='has_changed',
            field=models.BooleanField(default=True, help_text='True, если изменения есть, False, если изменений нет', verbose_name='Есть изменения, не отправленные на Яндекс'),
        ),
        migrations.AddField(
            model_name='price',
            name='has_changed',
            field=models.BooleanField(default=True, help_text='True, если изменения есть, False, если изменений нет', verbose_name='Есть изменения, не отправленные на Яндекс'),
        ),
    ]