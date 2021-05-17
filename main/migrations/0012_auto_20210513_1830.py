# Generated by Django 3.1.7 on 2021-05-13 15:30

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_price_net_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='availability',
            field=models.CharField(blank=True, choices=[('ACTIVE', 'Поставки будут'), ('INACTIVE', 'Товар есть на складе, и его поставок не будет'), ('DELISTED', 'Архив: товар закончился на складе, и его поставок больше не будет.')], max_length=8, null=True, verbose_name='Планы по поставкам'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='name',
            field=models.CharField(help_text='Составляйте по схеме: тип товара + бренд или производитель + модель +\n                                      отличительные характеристики.', max_length=255, null=True, verbose_name='Название товара'),
        ),
        migrations.AlterField(
            model_name='price',
            name='currencyId',
            field=models.CharField(choices=[('RUR', 'Руб.')], default='R', max_length=3, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='price',
            name='vat',
            field=models.IntegerField(blank=True, choices=[(2, '10 %'), (5, '0 %'), (6, 'не облагается'), (7, '20 %')], help_text='Если параметр не указан, используется ставка НДС, установленная в личном кабинете магазина.', null=True, verbose_name='НДС'),
        ),
        migrations.AlterField(
            model_name='processingstatenote',
            name='type',
            field=models.CharField(choices=[('ASSORTMENT', 'Товар производится в разных вариантах. Каждый из них нужно описать как отдельный товар'), ('CANCELLED', 'Товар отозван с модерации по вашей инициативе'), ('CONFLICTING_INFORMATION', 'Вы предоставили противоречивую информацию о товаре.'), ('DEPARTMENT_FROZEN', 'Правила размещения товаров в данной категории перерабатываются,'), ('INCORRECT_INFORMATION', "Информация о товаре, которую вы предоставили, противоречит'\n                                                        описанию от производителя."), ('LEGAL_CONFLICT', 'Товар не прошел модерацию по юридическим причинам.'), ('NEED_CLASSIFICATION_INFORMATION', 'Информации о товаре, которую вы \n                                            предоставили, не хватает, чтобы отнести его к категории'), ('NEED_INFORMATION', 'Товар раньше не продавался в России и пока не размещается на Маркете.'), ('NEED_PICTURES', 'Для идентификации товара нужны его изображения'), ('NEED_VENDOR', 'Неверно указан производитель товара'), ('NO_CATEGORY', 'Товары из указанной категории пока не размещаются на Маркете.'), ('NO_KNOWLEDGE', ''), ('NO_PARAMETERS_IN_SHOP_TITLE', 'Товар производится в разных вариантах, и из указанного названия непонятно, о каком идет речь.'), ('NO_SIZE_MEASURE', 'Для этого товара нужна размерная сетка. Отправьте ее в службу поддержки'), ('UNKNOWN', 'Товар не прошел модерацию по другой причине. Обратитесь в службу поддержки или к вашему менеджеру')], max_length=31, null=True, verbose_name='Тип причины, по которой товар не прошел модерацию'),
        ),
    ]
