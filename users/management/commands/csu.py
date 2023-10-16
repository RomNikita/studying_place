from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin1@admin.com',
            first_name='Admin',
            last_name='Adminov',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('12345qwe')
        user.save()