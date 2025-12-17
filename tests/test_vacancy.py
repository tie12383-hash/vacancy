import pytest
import sys
import os

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.vacancy import Vacancy  # noqa: E402


class TestVacancy:
    """Тесты для класса Vacancy"""

    def test_create_vacancy(self):
        """Тест создания вакансии"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            description="Разработка на Python",
            requirements="Опыт от 3 лет",
            company="ООО Технологии",
        )

        assert vacancy.title == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.avg_salary == 125000

    def test_create_vacancy_without_salary(self):
        """Тест создания вакансии без зарплаты"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            description="Разработка на Python",
        )

        assert vacancy.salary_from is None
        assert vacancy.salary_to is None
        assert vacancy.avg_salary == 0.0

    def test_validation_title(self):
        """Тест валидации названия"""
        with pytest.raises(ValueError):
            Vacancy(title="", url="https://hh.ru/vacancy/123")

    def test_validation_url(self):
        """Тест валидации URL"""
        with pytest.raises(ValueError):
            Vacancy(title="Developer", url="invalid_url")

    def test_validation_salary(self):
        """Тест валидации зарплаты"""
        with pytest.raises(ValueError):
            Vacancy(
                title="Developer", url="https://hh.ru/vacancy/123", salary_from=-1000
            )

    def test_comparison(self):
        """Тест сравнения вакансий"""
        vacancy1 = Vacancy(
            title="Junior Python",
            url="https://hh.ru/vacancy/1",
            salary_from=50000,
            salary_to=70000,
        )

        vacancy2 = Vacancy(
            title="Senior Python",
            url="https://hh.ru/vacancy/2",
            salary_from=150000,
            salary_to=200000,
        )

        assert vacancy1 < vacancy2
        assert vacancy2 > vacancy1
        assert vacancy1 != vacancy2

    def test_to_dict(self):
        """Тест конвертации в словарь"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
        )

        data = vacancy.to_dict()
        assert data["title"] == "Python Developer"
        assert data["url"] == "https://hh.ru/vacancy/123"
        assert data["salary_from"] == 100000

    def test_from_dict(self):
        """Тест создания из словаря"""
        data = {
            "title": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUR",
            "description": "Test",
            "requirements": "Test req",
            "company": "Test Company",
        }

        vacancy = Vacancy.from_dict(data)
        assert vacancy.title == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary_from == 100000

    def test_cast_to_object_list(self):
        """Тест конвертации данных API в список объектов"""
        hh_data = [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "description": "Test description",
                "snippet": {"requirement": "Python 3+"},
                "employer": {"name": "Test Company"},
            }
        ]

        vacancies = Vacancy.cast_to_object_list(hh_data)
        assert len(vacancies) == 1
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].title == "Python Developer"
