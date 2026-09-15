"""Функции сохранения и загрузки данных проекта в JSON-файлах."""

import json
from typing import Any


def load_doctors(filename: str) -> dict[int, dict[str, Any]]:
    """Загрузить врачей из JSON-файла.

    При отсутствии файла или повреждении JSON возвращает пустой словарь.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, данные не загружены")
        return {}
    return {int(doctor["id"]): doctor for doctor in data}


def save_doctors(filename: str, doctors: dict[int, dict[str, Any]]) -> None:
    """Сохранить врачей в JSON-файл."""
    data = [
        {"id": doctor_id, **doctor_data}
        for doctor_id, doctor_data in doctors.items()
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_appointments(filename: str) -> list[dict[str, Any]]:
    """Загрузить записи на прием из JSON-файла.

    При отсутствии файла или повреждении JSON возвращает пустой список.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, данные не загружены")
        return []


def save_appointments(
    filename: str, appointments: list[dict[str, Any]]
) -> None:
    """Сохранить записи на прием в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(appointments, file, ensure_ascii=False, indent=2)
