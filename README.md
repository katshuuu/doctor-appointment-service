# Сервис записи к врачу

Система онлайн-записи пациентов на прием к врачу на Python
с веб-интерфейсом на Django.

## 1. Назначение проекта

Сервис хранит сведения о врачах, специальностях, пациентах и записях
на прием. Консольная версия выполняет основные операции с объектами.
Веб-интерфейс показывает эти данные через шаблоны Django.

Проект развивается поэтапно: консольное приложение дополняется
веб-интерфейсом и постепенно переводится на возможности Django.

## 2. Используемые технологии

- Python 3;
- Django 5.2;
- Django ORM;
- Django Template Language (DTL);
- HTML5;
- CSS3;
- JavaScript;
- Bootstrap 5;
- JSON для консольной версии;
- SQLite;
- Git;
- pytest;
- flake8.

## 3. Предметная область

В системе четыре сущности:

- врач (`Doctor`) — идентификатор, имя и специальность;
- специальность — справочник `KNOWN_SPECIALTIES`;
- пациент (`Patient`) — имя и возраст;
- запись на прием (`Appointment`) — идентификатор, врач, пациент,
  дата, время и состояние записи.

Для предметной области реализованы собственные Python-классы.
Запись хранит объекты `Doctor` и `Patient`. Отменённая запись
остаётся в списке и не блокирует время приема.

Консольная версия по-прежнему читает JSON. Веб-интерфейс читает
те же сведения через модели Django ORM из базы `db.sqlite3`.
Исходная база ПР7 `data/doctor_appointment.sqlite` сохранена
и служит источником для переноса.

## 4. Структура проекта

```text
doctor-appointment-service/
├── apps/
│   ├── appointments/
│   │   └── templates/appointments/
│   │       ├── includes/appointment_status.html
│   │       ├── appointment_detail.html
│   │       └── appointment_list.html
│   ├── doctors/
│   │   └── templates/doctors/
│   │       ├── includes/doctor_card.html
│   │       ├── doctor_detail.html
│   │       └── doctor_list.html
│   ├── homepage/
│   │   ├── static/homepage/
│   │   │   ├── css/style.css
│   │   │   ├── img/logo.png
│   │   │   └── js/main.js
│   │   └── templates/homepage/index.html
│   ├── patients/
│   │   └── templates/patients/
│   └── specialties/
│       └── templates/specialties/
├── templates/
│   ├── includes/navigation.html
│   ├── 404.html
│   └── base.html
├── entities/
├── data/
│   ├── appointments.json
│   ├── doctors.json
│   └── doctor_appointment.sqlite
├── db/
│   ├── database.py
│   ├── import_json.py
│   ├── inspect_source_db.py
│   └── import_sqlite_to_orm.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── tests/
├── appointment_service/
│   ├── settings.py
│   └── urls.py
├── main.py
├── storage.py
├── utils.py
├── doctors.py
├── appointments.py
├── manage.py
└── README.md
```

Django-приложения лежат в пакете `apps/`. Так они не пересекаются
с модулями ПР3 `doctors.py` и `appointments.py` в корне репозитория.

Пациент получил собственное приложение: это сущность проекта, а не
встроенная модель пользователя Django. Специальность тоже вынесена
в приложение, потому что в проекте это отдельная сущность.

## 5. Веб-интерфейс

Веб-часть приложения реализована на Django.

Основные страницы:

- главная страница;
- список врачей и карточка врача;
- список специальностей и врачи выбранной специальности;
- список пациентов и карточка пациента;
- список записей и карточка записи;
- поиск свободных врачей на выбранную дату;
- статистика записей.

Для формирования страниц используются Django-шаблоны.
Генерация HTML непосредственно в Python-коде веб-представлений
не используется. Функция `page()` больше не используется
веб-представлениями.

Представления подготавливают данные и передают их в шаблоны
через контекст. Если объект не найден, представление передаёт
пустую переменную и статус 404, а текст «не найден» выводит шаблон.

Для неизвестного адреса подключён `handler404`
(`page_not_found()`). Он срабатывает при `DEBUG = False`.

## 6. Django Template Language

Шаблоны используют возможности Django Template Language.

### Базовый шаблон

Общий шаблон страниц: `templates/base.html`.
Он содержит HTML-структуру, Bootstrap, собственные CSS и JavaScript,
навигацию и блоки для содержимого отдельных страниц.

Дочерние шаблоны используют наследование:

```django
{% extends "base.html" %}
```

Содержимое страницы размещается в блоке `{% block content %}`.
Заголовок задаётся блоком `{% block title %}`.

### Включаемые шаблоны

Повторяющиеся фрагменты вынесены в отдельные шаблоны:

- `doctors/includes/doctor_card.html` — карточка врача;
- `specialties/includes/specialty_card.html` — строка справочника;
- `patients/includes/patient_card.html` — карточка пациента;
- `appointments/includes/appointment_status.html` — статус записи;
- `includes/navigation.html` — навигация.

### Контекст

Представления передают данные через словарь контекста.
Например, список врачей доступен как `{% for doctor in doctors %}`.
Карточка врача использует переменную `doctor`.
Тот же подход применяется к специальностям, пациентам и записям.

### Циклы и условия

Списки формируются циклом `{% for %}`.
При отсутствии элементов используется `{% empty %}`.
Условия `{% if %}` показывают найденный объект, пустую страницу 404
и состояние записи.

## 7. Фильтры шаблонов

В шаблонах используются стандартные фильтры Django Template Language.

Количество объектов:

```django
{{ doctors|length }}
```

Значение по умолчанию:

```django
{{ doctor.name|default:"Без имени" }}
```

Дата и время в базе хранятся текстом `YYYY-MM-DD` и `HH:MM:SS`
и выводятся как есть: фильтр `date` не разбирает такую строку.
Фильтры `|length` и `|default` по-прежнему используются в списках.
Проверка слота на карточке врача остаётся в Python
и повторяет правило `is_slot_available()`: отменённая запись
время не занимает.

## 8. URL-маршрутизация

Для страниц используются именованные маршруты и пространства имён:

```django
{% url 'doctors:list' %}
{% url 'doctors:detail' doctor.id %}
{% url 'specialties:detail' doctor.specialty %}
{% url 'patients:detail' patient.id %}
{% url 'doctors:available' %}
{% url 'appointments:statistics' %}
{% url 'appointments:detail' appointment.id %}
```

Пространства имён задаются через `app_name` в `urls.py` приложений:
`homepage`, `doctors`, `specialties`, `patients`, `appointments`.
Ссылки в шаблонах формируются через `{% url %}`, а не за счёт
жёстко заданных адресов.

## 9. Статические файлы

Статические файлы проекта находятся в каталоге
`apps/homepage/static/homepage/`.

Используются:

- `css/style.css` — собственные стили карточек, статуса и подвала;
- `js/main.js` — подставляет текущий год в подвал;
- `img/logo.png` — логотип сервиса.

В шаблонах для них нужен `{% load static %}`.
Bootstrap сохранён для базовой вёрстки. Оформление карточек
и статуса записи задаёт собственный CSS проекта.

## 10. Хранение данных

Консольное приложение хранит данные в JSON:

- `data/doctors.json` — 15 врачей;
- `data/appointments.json` — 15 записей, из них 3 отменены
  (идентификаторы 3, 7 и 12).

Веб-интерфейс работает с базой Django `db.sqlite3` через ORM.
Файл не хранится в Git: таблицы создают миграции.

Модели:

- `Specialty` — специальность, уникальное поле `name`;
- `Doctor` — врач, внешний ключ `specialty`
  (`on_delete=PROTECT`, `related_name="doctors"`);
- `Patient` — пациент, поля `name` и `age`;
- `Appointment` — запись, внешние ключи `doctor` и `patient`
  (`on_delete=PROTECT`, `related_name="appointments"`),
  дата, время и признак отмены `is_cancelled` (по умолчанию ложь).

Первичный ключ каждой модели — поле `id`.
Удалить врача, пациента или специальность, пока на них есть записи,
нельзя. Отмена записи не удаляет строку: метод `Appointment.cancel()`
ставит `is_cancelled`.

Исходная база ПР7 остаётся в `data/doctor_appointment.sqlite`.
Её по-прежнему собирает `python -m db.import_json` из JSON.
Резервная копия: `data/doctor_appointment_backup.sqlite`.
В целевую базу Django данные переносятся так:

```text
python manage.py migrate
python db/import_sqlite_to_orm.py
```

Структуру исходной базы показывает `python db/inspect_source_db.py`.
Файлы `sql/schema.sql`, `sql/queries.sql` и `db/queries.py`
сохранены как описание слоя ПР7. Страницы сайта их больше не вызывают.

## 11. Основные модули

- `storage.py` — загрузка и сохранение JSON;
- `entities/` — классы `Doctor`, `Patient`, `Appointment`
  и справочник специальностей;
- `main.py` — консольный интерфейс;
- `utils.py` — ввод в консольном интерфейсе;
- `doctors.py`, `appointments.py` — операции предметной области;
- `db/database.py` — подключение к исходной базе ПР7;
- `db/import_json.py` — перенос JSON в исходную базу;
- `db/import_sqlite_to_orm.py` — перенос исходной базы в ORM;
- `db/queries.py` — тексты SQL-запросов ПР7;
- `apps/*/models.py` — модели Django;
- `apps/*/views.py` — ORM-запросы и контекст шаблонов;
- `apps/homepage/views.py` — главная страница и обработчик 404.

## 12. Тестирование

В каталоге `tests/` находятся тесты классов предметной области
и страниц веб-интерфейса.

```text
pytest -v
```

## 13. Проверка качества кода

```text
flake8 . --extend-exclude=venv
```

## 14. Запуск проекта

Для запуска Django-сервера:

```text
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python db/import_sqlite_to_orm.py
python manage.py runserver
```

После запуска веб-интерфейс доступен по адресу
http://127.0.0.1:8000/.

Консольная версия:

```text
python main.py
```

## 15. Работа с Git

Исходный код проекта хранится в Git-репозитории.
Коммиты седьмой практической работы начинаются с префикса `PR7:`.
Коммиты девятой практической работы начинаются с префикса `PR9:`.

## 16. Текущее состояние проекта

На текущем этапе сервис содержит:

- предметные классы врача, пациента и записи, справочник специальностей;
- консольный интерфейс;
- хранение консольных данных в JSON;
- база SQLite, первичные и внешние ключи;
- импорт JSON в таблицы;
- SQL-запросы ПР7 в `sql/queries.sql`;
- модели Django, связи и миграции;
- перенос данных ПР7 в базу Django;
- ORM-запросы: списки, поиск, фильтры, сортировка,
  агрегаты, аннотации и постраничный список записей;
- поиск свободных врачей на дату и страница статистики;
- Django-проект и веб-представления четырёх сущностей;
- Django Template Language;
- наследование шаблонов и базовый шаблон `base.html`;
- блоки шаблонов и включаемые шаблоны;
- циклы, условия и фильтры шаблонов;
- именованные URL и пространства имён;
- статические CSS, JavaScript и логотип;
- собственное оформление интерфейса;
- тесты предметной области и веб-страниц.

Веб-страницы читают модели через Django ORM.
Создание, изменение и удаление доступны в административном
интерфейсе Django и при переносе данных.
Публичные формы создания записи в эту версию не входят.

## 17. ORM-запросы сайта

Запросы разнесены по представлениям и используются страницами:

1. Список врачей: `Doctor.objects.select_related("specialty").order_by("pk")`.
2. Поиск врача по имени: `filter(name__icontains=...)`.
3. Карточка врача: `Doctor.objects.get(pk=...)`.
4. Записи врача: `Appointment.objects.filter(doctor_id=...)`.
5. Занятые врачи на дату: `filter(appointment_date=..., is_cancelled=False)`.
6. Свободные врачи: `Doctor.objects.exclude(pk__in=...)`.
7. Специальности с числом врачей: `annotate(doctor_count=Count("doctors"))`.
8. Специальность по названию: `Specialty.objects.get(name=...)`.
9. Врачи специальности: `filter(specialty__name=...)`.
10. Список пациентов: `Patient.objects.order_by("pk")`.
11. Несовершеннолетние: `filter(age__lt=18)`.
12. Карточка пациента: `Patient.objects.get(pk=...)`.
13. Записи пациента, сортировка по дате и времени.
14. Карточка записи: `select_related("doctor", "patient")`.
15. Список записей: поиск по имени врача или пациента, фильтры,
    сортировка по белому списку полей, `Paginator`.
16. Сводка возраста: `Patient.objects.aggregate(Count, Avg, Min, Max)`.
17. Статистика врачей: `annotate(Count(...))` и `values()`.
18. Врачи больше чем с одной активной записью: `filter(appointments_count__gt=1)`.
19. Число активных записей: `aggregate(Count)`.

## 18. Дальнейшее развитие

JSON остаётся источником для консольной версии.
Дальше веб-приложение может получить публичные формы
создания и отмены записи, проверку ввода и API.
