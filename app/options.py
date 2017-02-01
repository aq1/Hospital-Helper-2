import os
import sys
import json

STRUCTURE_KEY = 'structure'
FIRST_START_KEY = 'first_start'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.dirname(sys.executable)
DATABASE = os.path.join(DATABASE_DIR, 'data.sqlite3')
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_FILE = os.path.join(DATABASE_DIR, 'error.log')

# klient left here intentionally
CLIENT_TABLE_NAME = 'klient'

CONCLUSION = 'Заключение: '
TEMPLATE_GLOBAL_STYLE = {
    'font-size': '11pt',
    'line-height': '11pt',
}

STATIC_DIR = os.path.join(BASE_DIR, 'gui', 'static')
REPORTS_DIR = os.path.join(DATABASE_DIR, 'reports')

TYPES = {
    'str': str,
    'float': float,
    'int': int,
    'list': list,
    'tuple': tuple
}

FIRST_START_WELCOME_TEXT = 'Добро пожаловать в Hospital Helper 2!\n' \
                           'Похоже, вы запустили программу впервые.\n' \
                           'Хотите загрузить стандартные шаблоны?'

INIT_TEMPLATES_PATH = os.path.join(DATA_DIR, 'init_templates.json')

with open(os.path.join(DATA_DIR, 'init_structure.json'), 'rb') as f:
    INIT_STRUCTURE = f.read().decode('utf8')

with open(os.path.join(DATA_DIR, 'translation.json'), 'rb') as f:
    TRANSLATION = json.loads(f.read().decode('utf8'))

# Order matters
CONTROL_BUTTONS_LABELS = [
    {'sys': 'data', 'ru': 'Данные', 'en': 'Data'},
    {'sys': 'report', 'ru': 'Отчет', 'en': 'Report'},
    {'sys': 'db', 'ru': 'База', 'en': 'DB'},
    {'sys': 'options', 'ru': 'Настройки', 'en': 'Options'},
]
