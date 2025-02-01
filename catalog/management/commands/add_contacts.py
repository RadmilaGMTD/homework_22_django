from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Contact


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Contact.objects.all().delete()
        call_command("loaddata", "contact_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
