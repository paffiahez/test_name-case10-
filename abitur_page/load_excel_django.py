import sys
from datetime import datetime, date
from pathlib import Path

import pandas as pd
from django.utils.text import slugify

from .models import Offer

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


def row_to_kwargs(row):
    """Собирает словарь {поле модели: значение} из строки Excel."""
    kwargs = {}
    for excel_name, field in COLUMN_MAP.items():
        if excel_name not in row or (isinstance(row[excel_name], float) and pd.isna(row[excel_name])):
            continue
        v = row[excel_name]
        if field in DATE_FIELDS:
            kwargs[field] = parse_date(v)
        elif field in INT_FIELDS:
            kwargs[field] = parse_int(v)
        else:
            kwargs[field] = clean(v)
    return kwargs


def import_file(path: Path):
    df = pd.read_excel(path, dtype=object)
    df.columns = [str(c).strip().lower() for c in df.columns]
    df = df.where(df.notna(), None)

    today = date.today()
    created_n = updated_n = skipped = 0

    for i, row in df.iterrows():
        kwargs = row_to_kwargs(row)

        if not kwargs.get("code") or not kwargs.get("employer"):
            print(f"{path.name}, строка {i + 2}: нет кода или предприятия — пропущена")
            skipped += 1
            continue

        active_cell = clean(row.get("активно", "")).lower()
        if active_cell in ("да", "1", "true", "активно"):
            kwargs["is_active"] = True
        elif active_cell in ("нет", "0", "false"):
            kwargs["is_active"] = False
        elif kwargs.get("end_date") and kwargs["end_date"] < today:
            kwargs["is_active"] = False

        # Стабильный ключ записи: код + работодатель + программа.
        slug_base = slugify(
            f"{kwargs['code']}-{kwargs['employer']}-{kwargs.get('name', '')}",
            allow_unicode=True,
        ) or "offer"
        slug_base = slug_base[:50]

        obj, created = Offer.objects.get_or_create(slug=slug_base, defaults={**kwargs})
        if not created:
            changed = False
            for field, value in kwargs.items():
                if getattr(obj, field) != value:
                    setattr(obj, field, value)
                    changed = True
            if changed:
                obj.save()
            updated_n += 1
        else:
            created_n += 1

    print(f" {path.name}: создано {created_n}, обновлено {updated_n}, пропущено {skipped}")


if __name__ == "__main__":
    files = sys.argv[1:] or [str(p) for p in Path("data/inbox").glob("*.xlsx")]
    if not files:
        print("Укажи путь к файлу: python manage.py shell < load_excel_django.py")
    for f in files:
        import_file(Path(f))
    print(f"Всего в базе: {Offer.objects.count()}")
