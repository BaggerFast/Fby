from django.core.management import BaseCommand
from main.view.others import db_to_exel


class Command(BaseCommand):

    help = "Generate reports for all dbs"

    def handle(self, *args, **options):
        db_to_exel("SELECT username AS 'Имя пользователя',"
                   "email AS 'Электронная почта',"
                   "CASE is_superuser WHEN 1 THEN 'Да' ELSE 'Нет' END AS 'Суперюзер'"
                   "FROM auth_user", 'auth_user.xlsx')
