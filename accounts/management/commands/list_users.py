from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Display all users in the database'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            self.stdout.write(self.style.SUCCESS(f'Username: {user.username}, Email: {user.email}'))
