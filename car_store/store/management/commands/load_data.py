from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):

    help = ""

    def handle(self, *args, **options):
        self.stdout.write("Done")
