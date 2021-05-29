"""
Команда для создания суперпользователя

Параметры:
-n, --name NAME- задать username=NAME для пользователя, если не задан - username=vasya
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    Cоздать суперпользователя
    """

    username = 'vasya'
    password = 'promprog'
    email = '1@abc.net'

    help = f'Create superuser {username} (password: {password}, email: {email})'

    def add_arguments(self, parser):
        """Определяем параметры"""
        parser.add_argument('-n', '--name', type=str, help='Username для создаваемого пользователя')

    def handle(self, *args, **options):
        name = options['name']
        if name:
            self.username = name
        get_user_model().objects.create_superuser(self.username, self.email, self.password)
        self.stdout.write(self.style.SUCCESS(f'Суперпользователь {self.username} успешно создан'))
