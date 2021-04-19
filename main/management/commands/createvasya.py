from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """Create superuser vasya"""

    username = 'vasya'
    password = 'promprog'
    email = '1@abc.net'

    help = f'Create superuser {username} (password: {password}, email: {email})'

    def handle(self, *args, **options):
        get_user_model().objects.create_superuser(self.username, self.email, self.password)
