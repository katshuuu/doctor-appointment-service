"""Каркас HTML-страниц и главная страница."""

from html import escape

from django.http import HttpResponse


def page(title, content):
    """Собрать HTML-документ: Bootstrap, свои стили и навигация."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    safe_title = escape(title)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{safe_title}</title>
    <link rel="stylesheet" href="{bootstrap}">
    <style>
        body {{ background-color: #f8f9fa; }}
        nav.nav {{ background-color: #0d6efd; }}
        nav.nav .nav-link {{ color: #fff; }}
    </style>
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/doctors/">Врачи</a>
        <a class="nav-link" href="/specialties/">Специальности</a>
        <a class="nav-link" href="/patients/">Пациенты</a>
        <a class="nav-link" href="/appointments/">Записи</a>
    </nav>
    <main class="container py-4">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница: описание сервиса и переход к разделам."""
    content = """
    <h1 class="display-4">Сервис записи к врачу</h1>
    <p class="lead">Онлайн-запись пациентов на прием к врачу.</p>
    <p>
        В сервисе четыре сущности предметной области:
        врач, специальность, пациент и запись на прием.
    </p>
    <p>Основные разделы:</p>
    <a href="/doctors/" class="btn btn-primary me-2 mb-2">Врачи</a>
    <a href="/specialties/" class="btn btn-primary me-2 mb-2">
        Специальности
    </a>
    <a href="/patients/" class="btn btn-primary me-2 mb-2">Пациенты</a>
    <a href="/appointments/" class="btn btn-secondary mb-2">Записи</a>
    """
    return HttpResponse(page("Сервис записи к врачу", content))


def page_not_found(request, exception):
    """Собственная страница для адреса, которому нет маршрута."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
