from django.core.management.base import BaseCommand

from catalog.data import NOTES, PROGRAMS
from catalog.models import Program, ProgramNote


class Command(BaseCommand):
    help = 'Загружает направления целевого обучения и заметки'

    def handle(self, *args, **options):
        for item in PROGRAMS:
            Program.objects.update_or_create(
                code=item['code'],
                defaults=item,
            )

        ProgramNote.objects.all().delete()
        for code, order, label, text in NOTES:
            ProgramNote.objects.create(
                program=Program.objects.get(code=code),
                order=order,
                label=label,
                text=text,
            )

        self.stdout.write(self.style.SUCCESS(
            f'Загружено направлений: {len(PROGRAMS)}, заметок: {len(NOTES)}'
        ))

