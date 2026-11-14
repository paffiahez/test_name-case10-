# catalog/management/commands/import_offers.py
import hashlib
from datetime import datetime, date
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from abitur_page.models import Offer

COLUMN_MAP = {
    "код направления": "code",
    "код": "code",
    "направление": "code",
    "название направления": "title",
    "название программы": "name",
    "программа": "name",
    "предприятие": "employer",
    "работодатель": "employer",
    "адрес предприятия": "employer_address",
    "адрес": "employer_address",
    "начало приёма заявок": "start_date",
    "окончание приёма заявок": "end_date",
    "количество целевых мест": "total_places",
    "количество мест": "total_places",
    "количество поданных заявок": "total_applications",
}

DATE_FIELDS = {"start_date", "end_date"}
INT_FIELDS = {"total_places", "total_applications"}


def parse_date(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    s = str(value).strip()
    for fmt in ("%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def parse_int(value):
    try:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return None
        return int(float(str(value).replace(",", ".").replace(" ", "")))
    except (ValueError, TypeError):
        return None


def clean(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


class Command(BaseCommand):
    help = "Импорт предложений о целевом обучении из Excel-файлов"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir", default="data/inbox",
            help="Папка с .xlsx файлами (по умолчанию data/inbox)",
        )
        parser.add_argument(
            "--file", help="Импорт одного конкретного файла",
        )

    def handle(self, *args, **options):
        if options["file"]:
            files = [Path(options["file"])]
        else:
            files = sorted(Path(options["dir"]).glob("*.xlsx"))

        if not files:
            self.stdout.write(self.style.WARNING(
                f"В папке {options['dir']} нет .xlsx файлов"
            ))
            return

        for path in files:
            self.import_file(path)

        self.stdout.write(self.style.SUCCESS(
            f"Всего в базе: {Offer.objects.count()}"
        ))

    def import_file(self, path: Path):
        df = pd.read_excel(path, dtype=object)
        df.columns = [str(c).strip().lower() for c in df.columns]
        df = df.where(df.notna(), None)

        today = date.today()
        created_n = updated_n = skipped = 0

        for i, row in df.iterrows():
            kwargs = {}
            for excel_name, field in COLUMN_MAP.items():
                v = row.get(excel_name)
                if v is None or (isinstance(v, float) and pd.isna(v)):
                    continue
                if field in DATE_FIELDS:
                    kwargs[field] = parse_date(v)
                elif field in INT_FIELDS:
                    kwargs[field] = parse_int(v)
                else:
                    kwargs[field] = clean(v)

            if not kwargs.get("code") or not kwargs.get("employer"):
                self.stdout.write(self.style.WARNING(
                    f"! {path.name}, строка {i + 2}: нет кода или предприятия — пропущена"
                ))
                skipped += 1
                continue

            active_cell = clean(row.get("активно", "")).lower()
            if active_cell in ("да", "1", "true", "активно"):
                kwargs["is_active"] = True
            elif active_cell in ("нет", "0", "false"):
                kwargs["is_active"] = False
            elif kwargs.get("end_date") and kwargs["end_date"] < today:
                kwargs["is_active"] = False

            slug_base = slugify(
                f"{kwargs['code']}-{kwargs['employer']}-{kwargs.get('name', '')}",
                allow_unicode=True,
            )[:50] or "offer"

            obj, created = Offer.objects.get_or_create(slug=slug_base, defaults=kwargs)
            if created:
                created_n += 1
            else:
                changed = False
                for field, value in kwargs.items():
                    if getattr(obj, field) != value:
                        setattr(obj, field, value)
                        changed = True
                if changed:
                    obj.save()
                updated_n += 1

        self.stdout.write(self.style.SUCCESS(
            f"{path.name}: создано {created_n}, обновлено {updated_n}, пропущено {skipped}"
        ))
