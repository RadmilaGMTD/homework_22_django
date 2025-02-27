from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Contact


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Contact.objects.all().delete()
        call_command("loaddata", "contacts_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
