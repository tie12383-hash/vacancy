import json
import os
from typing import List, Dict, Any
from ..models.vacancy import Vacancy
from .abstract_storage import AbstractStorage


class JSONStorage(AbstractStorage):
    """Класс для работы с JSON-файлом"""

    def __init__(self, filename: str = "data/vacancies.json"):
        self._filename = filename
        self._ensure_directory()
        self._vacancies: List[Dict[str, Any]] = self._load_from_file()

    def _ensure_directory(self) -> None:
        """Создает директорию для файла, если она не существует"""
        directory = os.path.dirname(self._filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _load_from_file(self) -> List[Dict[str, Any]]:
        """Загружает данные из JSON-файла"""
        if os.path.exists(self._filename):
            try:
                with open(self._filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def _save_to_file(self) -> None:
        """Сохраняет данные в JSON-файл"""
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(self._vacancies, f, ensure_ascii=False, indent=2)

    def _vacancy_to_dict(self, vacancy: Vacancy) -> Dict[str, Any]:
        """Конвертирует вакансию в словарь для хранения"""
        return vacancy.to_dict()

    def _is_duplicate(self, vacancy_dict: Dict[str, Any]) -> bool:
        """Проверяет, есть ли дубликат вакансии"""
        for existing in self._vacancies:
            if existing.get("url") == vacancy_dict.get("url") and existing.get(
                "title"
            ) == vacancy_dict.get("title"):
                return True
        return False

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл, если ее нет"""
        vacancy_dict = self._vacancy_to_dict(vacancy)

        if not self._is_duplicate(vacancy_dict):
            self._vacancies.append(vacancy_dict)
            self._save_to_file()

    def get_vacancies(self, **kwargs) -> List[Vacancy]:
        """
        Получает вакансии по критериям

        Args:
            **kwargs: Критерии фильтрации:
                - keyword: ключевое слово в описании
                - salary_min: минимальная зарплата
                - salary_max: максимальная зарплата
                - company: название компании

        Returns:
            Список вакансий
        """
        filtered_data = self._vacancies.copy()

        # Фильтрация по ключевому слову
        if keyword := kwargs.get("keyword"):
            filtered_data = [
                v
                for v in filtered_data
                if keyword.lower() in v.get("description", "").lower()
                or keyword.lower() in v.get("requirements", "").lower()
                or keyword.lower() in v.get("title", "").lower()
            ]

        # Фильтрация по зарплате
        if salary_min := kwargs.get("salary_min"):
            filtered_data = [
                v
                for v in filtered_data
                if v.get("salary_from") and v.get("salary_from") >= salary_min
            ]

        if salary_max := kwargs.get("salary_max"):
            filtered_data = [
                v
                for v in filtered_data
                if v.get("salary_to") and v.get("salary_to") <= salary_max
            ]

        # Фильтрация по компании
        if company := kwargs.get("company"):
            filtered_data = [
                v
                for v in filtered_data
                if company.lower() in v.get("company", "").lower()
            ]

        # Конвертация в объекты Vacancy
        return [Vacancy.from_dict(data) for data in filtered_data]

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из файла"""
        vacancy_dict = self._vacancy_to_dict(vacancy)

        self._vacancies = [
            v
            for v in self._vacancies
            if not (
                v.get("url") == vacancy_dict.get("url")
                and v.get("title") == vacancy_dict.get("title")
            )
        ]
        self._save_to_file()

    def clear(self) -> None:
        """Очищает файл"""
        self._vacancies = []
        self._save_to_file()
