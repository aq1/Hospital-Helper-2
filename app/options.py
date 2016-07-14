import os
import sys


STRUCTURE_KEY = 'structure'

# Order matters
CONTROL_BUTTONS_LABELS = (
    {'sys': 'data', 'ru': 'Данные', 'en': 'Data'},
    {'sys': 'report', 'ru': 'Отчет', 'en': 'Report'},
    {'sys': 'db', 'ru': 'База', 'en': 'DB'},
    {'sys': 'options', 'ru': 'Настройки', 'en': 'Options'},
)

TRANSLATION = (
    {'sys': 'weight', 'ru': 'Вес'},
    {'sys': 'age', 'ru': 'Возраст'},
    {'sys': 'user', 'ru': 'Врач'},
    {'sys': 'key', 'ru': 'Ключ'},
    {'sys': 'conclusion', 'ru': 'Заключение'},
    {'sys': 'hr', 'ru': 'ЧСС'},
    {'sys': 'date_of_birth', 'ru': 'Дата Рождения'},
    {'sys': 'name', 'ru': 'Имя'},
    {'sys': 'surname', 'ru': 'Фамилия'},
    {'sys': 'patronymic', 'ru': 'Отчество'},
    {'sys': 'group', 'ru': 'Группа'},
    {'sys': 'height', 'ru': 'Высота'},
    {'sys': 'header', 'ru': 'Заголовок'},
    {'sys': 'client', 'ru': 'Клиент'},
    {'sys': 'examined', 'ru': 'Осмотрен'},
    {'sys': 'organization', 'ru': 'Больница'},
    {'sys': 'body', 'ru': 'Текст'},
    {'sys': 'value', 'ru': 'Значение'},
    {'sys': 'template', 'ru': 'Шаблон'},
    {'sys': 'sent_by', 'ru': 'Направлен'},
    {'sys': 'item', 'ru': 'Объект'},
    {'sys': 'path', 'ru': 'Путь'},
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.dirname(sys.executable)
DATABASE = os.path.join(DATABASE_DIR, 'data.sqlite3')

# klient left here intentionally
CLIENT_TABLE_NAME = 'klient'

CONCLUSION = 'Заключение: '

STATIC_DIR = os.path.join(BASE_DIR, 'gui', 'static')
REPORTS_DIR = os.path.join(DATABASE_DIR, 'reports')

TYPES = {
    'str': str,
    'float': float,
    'int': int,
    'list': list,
    'tuple': tuple
}

INIT_STRUCTURE = """[
    {
        "name": "Клиент",
        "verbose_name": "",
        "db": true,
        "group": "Клиент",
        "relations": [
            "user"
        ],
        "args": [
            {
                "name": "Фамилия",
                "type": "str"
            },
            {
                "name": "Имя",
                "type": "str"
            },
            {
                "name": "Отчество",
                "type": "str"
            },
            {
                "name": "Возраст"
            },
            {
                "name": "Рост"
            },
            {
                "name": "Вес"
            },
            {
                "name": "Чсс"
            },
            {
                "name": "_ППТ",
                "calculation": "sqrt(Рост * Вес / 3600)"
            }
        ]
    },
    {
        "name": "Сердце",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Аорта"
            },
            {
                "name": "ОАК"
            },
            {
                "name": "ЛП"
            },
            {
                "name": "КДРЛЖ"
            },
            {
                "name": "КСРЛЖ"
            },
            {
                "name": "ЗСЛЖ"
            },
            {
                "name": "МЖП"
            },
            {
                "name": "АК"
            },
            {
                "name": "КЛА"
            },
            {
                "name": "ПП"
            },
            {
                "name": "ПЖ"
            },
            {
                "name": "НПВ"
            },
            {
                "name": "КДО",
                "calculation": "7 / (2.4 + (0.1 * КДРЛЖ)) * (0.1 * КДРЛЖ) ** 3"
            },
            {
                "name": "КСО",
                "calculation": "7 / (2.4 + 0.1 * КСРЛЖ) * 0.1 * КСРЛЖ ** 3"
            },
            {
                "name": "ФВ",
                "calculation": "((КДО - КСО) / КДО) * 100"
            },
            {
                "name": "ИММЛЖ",
                "calculation": "(0.8 * (1.04 * (sum((КДРЛЖ, МЖП, ЗСЛЖ)) ** 3) - КДРЛЖ ** 3) + 0.6) / Клиент._ППТ"
            },
            {
                "name": "ОТС",
                "calculation": "(2 * ЗСЛЖ) / КДРЛЖ"
            }
        ]
    },
    {
        "name": "Печень",
        "group": "Брюшная полость",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "КВР"
            },
            {
                "name": "ВВ"
            },
            {
                "name": "НПВ"
            },
            {
                "name": "Холедох"
            }
        ]
    },
    {
        "name": "Желчный",
        "group": "Брюшная полость",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Длина"
            },
            {
                "name": "Ширина"
            },
            {
                "name": "Толщина"
            },
            {
                "name": "Стенка"
            },
            {
                "name": "Объем",
                "calculation": "0.00052 * (Длина * Ширина * Толщина)"
            }
        ]
    },
    {
        "name": "Поджелудочная",
        "verbose_name": "Поджелудочная железа",
        "group": "Брюшная полость",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Головка"
            },
            {
                "name": "Тело"
            },
            {
                "name": "Хвост"
            },
            {
                "name": "Вирсунгов"
            }
        ]
    },
    {
        "name": "Селезенка",
        "group": "Брюшная полость",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Длина"
            },
            {
                "name": "Ширина"
            },
            {
                "name": "Толщина"
            },
            {
                "name": "Площадь"
            }
        ]
    },
    {
        "name": "Почки",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Длина"
            },
            {
                "name": "Ширина"
            },
            {
                "name": "Паренхим"
            },
            {
                "name": "Чашечки"
            },
            {
                "name": "Лоханка"
            },
            {
                "name": "Длина_2"
            },
            {
                "name": "Ширина_2"
            },
            {
                "name": "Паренхим_2"
            },
            {
                "name": "Чашечки_2"
            },
            {
                "name": "Лоханка_2"
            }
        ]
    },
    {
        "name": "Щитовидная",
        "verbose_name": "Щитовидная железа",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Перешеек"
            },
            {
                "name": "Длина"
            },
            {
                "name": "Ширина"
            },
            {
                "name": "Толщина"
            },
            {
                "name": "Объем",
                "calculation": "0.00048 * (Длина * Ширина * Толщина)"
            },
            {
                "name": "Длина_2"
            },
            {
                "name": "Ширина_2"
            },
            {
                "name": "Толщина_2"
            },
            {
                "name": "Объем_2",
                "calculation": "0.00048 * (Длина_2 * Ширина_2 * Толщина_2)"
            },
            {
                "name": "V_общ",
                "calculation": "Объем + Объем_2"
            }
        ]
    },
    {
        "name": "Предстательная",
        "verbose_name": "Предстательная железа",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Длина"
            },
            {
                "name": "Ширина"
            },
            {
                "name": "Толщина"
            },
            {
                "name": "Объем",
                "calculation": "0.00052 * (Длина * Ширина * Толщина)"
            }
        ]
    },
    {
        "name": "М.Пузырь",
        "verbose_name": "Мочевой пузырь",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Длина"
            },
            {
                "name": "Ширина"
            },
            {
                "name": "Толщина"
            },
            {
                "name": "Стенка"
            },
            {
                "name": "Объем",
                "calculation": "0.00052 * (Длина * Ширина * Толщина)"
            }
        ]
    },
    {
        "name": "Гинекология",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Матка длина"
            },
            {
                "name": "Матка ширина"
            },
            {
                "name": "Матка толщина"
            },
            {
                "name": "Шейка длина"
            },
            {
                "name": "Шейка толщина"
            },
            {
                "name": "Эндометрий"
            },
            {
                "name": "Л.Длина"
            },
            {
                "name": "Л.Ширина"
            },
            {
                "name": "Л.Толщина"
            },
            {
                "name": "П.Длина"
            },
            {
                "name": "П.Ширина"
            },
            {
                "name": "П.Толщина"
            },
            {
                "name": "Диаметр"
            },
            {
                "name": "М.Объем"
            },
            {
                "name": "Л.Объем"
            },
            {
                "name": "П.Объем"
            }
        ]
    },
    {
        "name": "Урология",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "П.Длина"
            },
            {
                "name": "П.Ширина"
            },
            {
                "name": "П.Толщина"
            },
            {
                "name": "Л.Длина"
            },
            {
                "name": "Л.Ширина"
            },
            {
                "name": "Л.Толщина"
            },
            {
                "name": "П.П.Длина"
            },
            {
                "name": "П.П.Толщина"
            },
            {
                "name": "Л.П.Длина"
            },
            {
                "name": "Л.П.Толщина"
            },
            {
                "name": "П.Объем"
            },
            {
                "name": "Л.Объем"
            }
        ]
    },
    {
        "name": "Образование",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Длина_1"
            },
            {
                "name": "Длина_2"
            },
            {
                "name": "Длина_3"
            },
            {
                "name": "Длина_4"
            },
            {
                "name": "Длина_5"
            },
            {
                "name": "Длина_6"
            }
        ]
    },
    {
        "name": "Киста",
        "db": false,
        "relations": [
            "Клиент"
        ],
        "args": [
            {
                "name": "Длина_1"
            },
            {
                "name": "Длина_2"
            },
            {
                "name": "Длина_3"
            },
            {
                "name": "Длина_4"
            },
            {
                "name": "Длина_5"
            },
            {
                "name": "Длина_6"
            },
            {
                "name": "Длина_7"
            },
            {
                "name": "Длина_8"
            }
        ]
    }
]"""
