"""
Команда для создания суперпользователя

Параметры:
-n, --name NAME- задать username=NAME для пользователя, усли не задан - username=vasya
-d, --db_save - восстановить из файлов бд для создаваемого пользователя
"""
import json

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from main.models_addon.save_dir import OfferPattern, OrderPattern, PricePattern, OfferReportPattern


def save_db_from_files(user: User):
    """Восстановление бд из файлов для пользователя user"""
    def get_json_data_from_file(file: str) -> dict:
        """Загрузка данных из файла file."""
        file = f'json_data/{file}.json'
        with open(file, "r", encoding="utf-8") as read_file:
            return json.load(read_file)['result']

    context = {
        OfferPattern: {'file': "offer_data", 'attrs': 'offerMappingEntries'},
        OrderPattern: {'file': "order_data", 'attrs': 'orders'},
        PricePattern: {'file': "price_data", 'attrs': 'offers'},
        OfferReportPattern: {'file': "offer_report_data", 'attrs': 'shopSkus'}
    }
    for pattern, attrs in context.items():
        pattern(json=get_json_data_from_file(file=attrs['file'])[attrs['attrs']]).save(user=user)


class Command(BaseCommand):
    """
    Cоздать суперпользователя
    """

    username = 'vasya'
    password = 'promprog'
    email = '1@abc.net'

    help = f'Create superuser {username} (password: {password}, email: {email})'

    def add_arguments(self, parser):
        """Опреднляем параметры"""
        parser.add_argument('-n', '--name', type=str, help='Username для создаваемого пользователя')
        parser.add_argument(
            '-d', '--db_save',
            action='store_true',
            help='Восстановить из файлов базу данных для создаваемого пользователя'
        )

    def handle(self, *args, **options):
        name = options['name']
        db_save = options['db_save']
        if name:
            self.username = name
        user = get_user_model().objects.create_superuser(self.username, self.email, self.password)
        self.stdout.write(self.style.SUCCESS(f'Суперпользователь {self.username} успешно создан'))
        if db_save:
            self.stdout.write(self.style.MIGRATE_HEADING(f'Восстанавливаю бд для {self.username}...'))
            save_db_from_files(user=user)
            self.stdout.write(self.style.SUCCESS(f'База данных для суперпользователя {self.username}'
                                                 f' успешно восстановлена'))
