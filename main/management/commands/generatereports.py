from django.core.management import BaseCommand
from main.view.others import db_to_excel


class Command(BaseCommand):

    help = "Generate reports for all dbs"

    columns_ru = {
        'id': 'ID',
        'username': 'Имя пользователя',
        'email': 'Электронная почта',
        'is_superuser': 'Супер-юзер',
        'marketSku': 'SKU маркета',
        'updatedAt': 'Обновлено',
        'shopSku': 'SKU магазина',
        'name': 'Имя',
        'category': 'Категория',
        'manufacturer': 'Производитель',
        'vendor': 'Продавец',
        'vendorCode': 'Код продавца',
        'description': 'Описание',
        'certificate': 'Сертификат',
        'availability': 'Доступность',
        'transportUnitSize': 'Размер юнита',
        'minShipment': 'Минимум',
        'quantumOfSupply': 'Количество',
        'deliveryDurationDays': 'Длительность доставки',
        'boxCount': 'Количество коробок',
        'user_id': 'ID пользователя',
    }
    map_bool = "WHEN 1 THEN 'Да' ELSE 'Нет' END"

    def select_ru(self, *args):
        sql_string = ""
        for column in args:
            sql_string += f" {column} AS '{self.columns_ru[column]}',"
        return sql_string[:-1]

    def handle(self, *args, **options):
        db_to_excel(
            'SELECT {} FROM main_offer'.format(
                self.select_ru(
                    'marketSku', 'updatedAt', 'shopSku', 'name', 'category', 'manufacturer',
                    'vendor', 'vendorCode', 'description', 'certificate', 'availability',
                    'transportUnitSize', 'minShipment', 'quantumOfSupply',
                    'deliveryDurationDays', 'boxCount', 'user_id'
                )
            ),
            'main_offer.xlsx'
        )
