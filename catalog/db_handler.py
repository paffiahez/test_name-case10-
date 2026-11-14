import json
import os
from django.conf import settings

# Путь к файлу базы данных (он лежит в корне проекта, рядом с manage.py)
DB_FILE = os.path.join(settings.BASE_DIR, 'database.json')

def load_data():
    """
    Читает данные из файла database.json.
    Если файла нет или он пустой — возвращает пустой словарь.
    """
    if not os.path.exists(DB_FILE):
        return {}
        
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Если файл поврежден или пуст, возвращаем пустоту
            return {}

def save_data(data):
    """
    Сохраняет переданные данные (словарь) в файл database.json.
    """
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        # ensure_ascii=False нужен, чтобы русские буквы сохранялись нормально, а не в виде \u0430...
        # indent=4 делает файл красивым и читаемым
        json.dump(data, f, ensure_ascii=False, indent=4)
