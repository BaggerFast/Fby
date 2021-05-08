# Generated by Django 3.1.7 on 2021-05-08 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210504_1607'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='barcode',
            name='barcode',
            field=models.CharField(blank=True, help_text='Штрихкод обязателен при размещении товара по модели FBY и FBY+.\n                                         Допустимые форматы: EAN-13, EAN-8, UPC-A, UPC-E, Code 128. Для книг\n                                          — ISBN-10 или ISBN-13. Для товаров определённых производителей передайте\n                                         только код GTIN. Если штрихкодов несколько, укажите их через запятую.', max_length=255, null=True, verbose_name='Штрихкод'),
        ),
        migrations.AlterField(
            model_name='commission',
            name='actual',
            field=models.DecimalField(decimal_places=2, help_text='Точность — два знака после запятой', max_digits=10, null=True, verbose_name='Сумма комиссии, которая была выставлена в момент создания заказа и которую нужно оплатить'),
        ),
        migrations.AlterField(
            model_name='commission',
            name='predicted',
            field=models.DecimalField(decimal_places=2, help_text='Точность — два знака после запятой', max_digits=10, null=True, verbose_name='Сумма комиссии, которая была бы выставлена, если бы заказ был создан в момент\n                        формирования отчета по заказам'),
        ),
        migrations.AlterField(
            model_name='inclusion',
            name='type',
            field=models.CharField(choices=[('FREE_EXPIRE', 'Товар,  у которого срок бесплатного хранения подходит к концу.'), ('PAID_EXPIRE', 'Товар, за хранение которого скоро придется платить по повышенному тарифу.'), ('PAID_EXTRA', 'Товар, который хранится платно по повышенному тарифу.')], max_length=11, null=True, verbose_name='Тип условий хранения и обработки товара на складе'),
        ),
        migrations.AlterField(
            model_name='initialitem',
            name='order',
            field=models.ForeignKey(help_text="В ходе обработки заказа Маркет может удалить из него единицы товаров —\n                  при проблемах на складе или по инициативе пользователя.\n                  Если из заказа удалены все единицы товара, его не будет в списке items —\n                  только в списке initialItems. '\n                  Если в заказе осталась хотя бы одна единица товара, он будет и в списке items\n                  (с уменьшенным количеством единиц count),\n                  и в списке initialItems (с первоначальным количеством единиц initialCount).", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initialItems', to='main.order', verbose_name='Список товаров в заказе до изменений'),
        ),
        migrations.AlterField(
            model_name='item',
            name='count',
            field=models.PositiveIntegerField(help_text='Если из заказа удалены все единицы товара, он попадет\n                                        только в список initialItems.', null=True, verbose_name='Количество единиц товара с учетом удаленных единиц'),
        ),
        migrations.AlterField(
            model_name='item',
            name='order',
            field=models.ForeignKey(help_text='В ходе обработки заказа Маркет может удалить из него единицы товаров —\n                  при проблемах на складе или по инициативе пользователя.\n                  Если из заказа удалены все единицы товара, его не будет в списке items —\n                  только в списке initialItems.\n                  Если в заказе осталась хотя бы одна единица товара, он будет и в списке items\n                  (с уменьшенным количеством единиц count), \n                  и в списке initialItems (с первоначальным количеством единиц initialCount).', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.order', verbose_name='Список товаров в заказе после возможных изменений'),
        ),
        migrations.AlterField(
            model_name='itemprice',
            name='type',
            field=models.CharField(choices=[('BUYER', 'Цена на товар с учетом скидок'), ('CASHBACK', 'Скидка по баллам Яндекс Плюс за шт.'), ('MARKETPLACE', 'Скидка по бонусам Маркета за шт.'), ('SPASIBO', 'Скидка по бонусам СберСпасибо за шт.')], max_length=11, null=True, verbose_name='Тип скидки или цена на товар'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='availability',
            field=models.CharField(blank=True, choices=[('ACTIVE', 'Поставки будут'), ('INACTIVE', 'Поставок не будет: товар есть на складе, но вы больше не планируете его поставлять.'), ('DELISTED', 'Архив: товар закончился на складе, и его поставок больше не будет.')], max_length=8, null=True, verbose_name='Планы по поставкам'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='boxCount',
            field=models.PositiveIntegerField(blank=True, help_text='Если нет — оставьте поле пустым. Если да — укажите количество\n                                           мест(например, кондиционер занимает 2 грузовых места — внешний и внутренний \n                                           блоки в двух коробках).', null=True, verbose_name='Товар занимает больше одного места'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='deliveryDurationDays',
            field=models.PositiveSmallIntegerField(blank=True, help_text='За сколько дней вы поставите товар на склад.', null=True, verbose_name='Срок поставки'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='quantumOfSupply',
            field=models.PositiveSmallIntegerField(blank=True, help_text='По сколько товаров можно добавлять к минимальной партии. Например, вы планируете поставлять\n                  детское питание партиями, причем к минимальной партии хотите прибавлять минимум по 2 коробки,\n                  а в каждой коробке по 6 баночек. Тогда добавочная партия — 12 баночек, а к минимальной партии\n                  можно добавлять 12, 24, 36 баночек и т. д.', null=True, verbose_name='Добавочная партия'),
        ),
        migrations.AlterField(
            model_name='order',
            name='creationDate',
            field=models.DateTimeField(help_text='Формат даты и времени: ISO 8601.\n                    Например, 2017-11-21T00:00:00. Часовой пояс — UTC+03:00 (Москва)', null=True, verbose_name='Дата и время создания заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paymentType',
            field=models.CharField(choices=[('CREDIT', 'Оформлен в кредит'), ('POSTPAID', 'Оплачен после получения'), ('PREPAID', 'Оплачен до получения')], max_length=8, null=True, verbose_name='Тип оплаты заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CANCELLED_BEFORE_PROCESSING', 'Отменён до обработки'), ('CANCELLED_IN_DELIVERY', 'Отменен во время его доставки'), ('CANCELLED_IN_PROCESSING', 'Отменен во время его обработки'), ('DELIVERY', 'Передан службе доставки'), ('DELIVERED', 'Доставлен'), ('PARTIALLY_RETURNED', 'Частично возвращен покупателем'), ('PICKUP', 'Доставлен в пункт выдачи'), ('PROCESSING', 'В обработке'), ('REJECTED', 'Создан, но не оплачен'), ('RETURNED', 'Полностью возвращен покупателем'), ('UNKNOWN', 'Неизвестный статус')], max_length=27, null=True, verbose_name='Текущий статус заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='statusUpdateDate',
            field=models.DateTimeField(help_text='Формат даты и времени: ISO 8601.\n                    Например, 2017-11-21T00:00:00. Часовой пояс — UTC+03:00 (Москва)', null=True, verbose_name='Дата и время, когда статус заказа был изменен в последний раз'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='source',
            field=models.CharField(choices=[('BUYER', 'покупателя'), ('CASHBACK', 'за скидку по баллам Яндекс.Плюса'), ('MARKETPLACE', 'за скидку маркетплейса'), ('SPASIBO', 'за скидку по бонусам СберСпасибо')], max_length=11, null=True, verbose_name='Способ денежного перевода'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='total',
            field=models.DecimalField(decimal_places=2, help_text='Значение указывается в рублях независимо от способа денежного перевода.\n                  Точность — два знака после запятой', max_digits=10, null=True, verbose_name='Сумма денежного перевода'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='type',
            field=models.CharField(choices=[('PAYMENT', 'Платеж'), ('REFUND', 'Возврат платежа')], max_length=7, null=True, verbose_name='Тип денежного перевода'),
        ),
        migrations.AlterField(
            model_name='price',
            name='currencyId',
            field=models.CharField(choices=[('RUR', 'Руб.')], max_length=3, null=True, verbose_name='Валюта, в которой указана цена на товар.'),
        ),
        migrations.AlterField(
            model_name='pricesuggestion',
            name='type',
            field=models.CharField(blank=True, choices=[('BUYBOX', 'Минимальная цена у партнеров на Маркете.'), ('DEFAULT_OFFER', 'Рекомендованная Маркетом цена, которая привлекает покупателей.'), ('MIN_PRICE_MARKET', 'Минимальная цена на Маркете'), ('MAX_DISCOUNT_BASE', 'Максимальная цена товара без скидки'), ('MARKET_OUTLIER_PRICE', 'Максимальная цена товара, которая обеспечивает показы на Маркете.')], max_length=21, null=True, verbose_name='Типы цен'),
        ),
        migrations.AlterField(
            model_name='processingstate',
            name='status',
            field=models.CharField(choices=[('READY', 'товар прошел модерацию. Чтобы разместить его на Маркете, установите для него цену и \n                        создайте поставку на склад.'), ('IN_WORK', 'Товар проходит модерацию. Может занять несколько дней'), ('NEED_CONTENT', 'для товара без SKU на Яндексе market_sku нужно найти карточку самостоятельно'), ('NEED_INFO', 'Товар не прошел модерацию из-за ошибок или недостающих сведений в описании товара.'), ('REJECTED', 'Товар не прошел модерацию, так как Маркет не планирует размещать подобные товары'), ('SUSPENDED', 'Товар не прошел модерацию, так как Маркет пока не размещает подобные товары'), ('OTHER', 'товар не прошел модерацию по другой причине. Обратитесь в службу поддержки или к вашему менеджеру')], help_text='Можно продавать или нет', max_length=12, null=True, verbose_name='Cтатус'),
        ),
        migrations.AlterField(
            model_name='processingstatenote',
            name='type',
            field=models.CharField(choices=[('ASSORTMENT', 'Товар производится в разных вариантах. Каждый из них нужно описать как отдельный товар'), ('CANCELLED', 'Товар отозван с модерации по вашей инициативе'), ('CONFLICTING_INFORMATION', 'Вы предоставили противоречивую информацию о товаре.'), ('DEPARTMENT_FROZEN', 'Правила размещения товаров в данной категории перерабатываются,'), ('INCORRECT_INFORMATION', "Информация о товаре, которую вы предоставили, противоречит'\n                                                        описанию от производителя."), ('LEGAL_CONFLICT', 'товар не прошел модерацию по юридическим причинам.'), ('NEED_CLASSIFICATION_INFORMATION', 'Информации о товаре, которую вы \n                                            предоставили, не хватает, чтобы отнести его к категории'), ('NEED_INFORMATION', 'Товар раньше не продавался в России и пока не размещается на Маркете.'), ('NEED_PICTURES', 'Для идентификации товара нужны его изображения'), ('NEED_VENDOR', 'Неверно указан производитель товара'), ('NO_CATEGORY', 'Товары из указанной категории пока не размещаются на Маркете.'), ('NO_KNOWLEDGE', ''), ('NO_PARAMETERS_IN_SHOP_TITLE', 'товар производится в разных вариантах, и из указанного названия непонятно, о каком идет речь.'), ('NO_SIZE_MEASURE', 'для этого товара нужна размерная сетка. Отправьте ее в службу поддержки'), ('UNKNOWN', 'товар не прошел модерацию по другой причине. Обратитесь в службу поддержки или к вашему менеджеру')], max_length=31, null=True, verbose_name='Тип причины, по которой товар не прошел модерацию'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='type',
            field=models.CharField(choices=[('AVAILABLE', 'Товар, доступный для продажи'), ('DEFECT', 'Товар с браком'), ('EXPIRED', 'Товар с истекшим сроком годности'), ('FIT', 'Товар, который доступен для продажи или уже зарезервирован'), ('FREEZE', 'Товар, который зарезервирован для заказов'), ('QUARANTINE', 'Товар, временно недоступный для продажи'), ('UTILIZATION', 'Товар, который будет утилизирован'), ('SUGGEST', 'Товар, который рекомендуется поставить на склад'), ('TRANSIT', 'Проданный товар')], max_length=11, null=True, verbose_name='Тип остатков товаров на складе'),
        ),
        migrations.AlterField(
            model_name='supplyscheduledays',
            name='supplyScheduleDay',
            field=models.CharField(choices=[('MONDAY', 'понедельник'), ('TUESDAY', 'вторник'), ('WEDNESDAY', 'среда'), ('THURSDAY', 'четверг'), ('FRIDAY', 'пятница'), ('SATURDAY', 'суббота'), ('SUNDAY', 'воскресенье')], help_text='Дни недели, когда вы готовы поставлять товары на склад маркетплейса.Заполняйте поле, чтобы получать рекомендации о пополнении товаров на складе.', max_length=9, null=True, verbose_name='Дни поставки'),
        ),
    ]
