"""Вспомогательные функции: преобразование и безопасный ввод данных."""

from datetime import date, time


def convert_age(age_input: str) -> int:
    """Преобразовать возраст пациента из строки в число (функция из ПР1)."""
    return int(age_input)


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число.

    При некорректном вводе запрос повторяется, программа не завершается
    аварийно.
    """
    while True:
        raw_value = input(prompt)
        try:
            return int(raw_value)
        except ValueError:
            print("Ошибка: введите целое число")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        raw_value = input(prompt)
        try:
            day_str, month_str, year_str = raw_value.split(".")
            return date(int(year_str), int(month_str), int(day_str))
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ")


def input_time(prompt: str) -> time:
    """Запросить у пользователя время в формате ЧЧ:ММ."""
    while True:
        raw_value = input(prompt)
        try:
            hour_str, minute_str = raw_value.split(":")
            return time(int(hour_str), int(minute_str))
        except ValueError:
            print("Ошибка: введите время в формате ЧЧ:ММ")
