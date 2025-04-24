from django.core.management.base import BaseCommand
from django.core.management import get_commands

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        commands = get_commands()
        self.stdout.write(f"{[command for command in commands.items() if command[1] == 'app']}")


    