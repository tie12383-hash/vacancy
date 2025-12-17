import sys
import os

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.vacancy import Vacancy  # noqa: E402
from src.utils.helpers import (  # noqa: E402
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
)


class TestHelpers:
    """Тесты вспомогательных функций"""

    def sample_vacancies(self):
        """Создание тестовых вакансий с разными зарплатами"""
        return [
            Vacancy(
                title="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                description="Python programming",
            ),
            Vacancy(
                title="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary_from=80000,
                description="Java programming",
            ),
            Vacancy(
                title="JavaScript Developer",
                url="https://hh.ru/vacancy/3",
                salary_from=90000,
                salary_to=110000,
                description="JavaScript programming",
            ),
        ]

    def test_filter_vacancies(self):
        """Тест фильтрации вакансий"""
        filtered = filter_vacancies(self.sample_vacancies(), ["Python"])
        assert len(filtered) == 1
        assert filtered[0].title == "Python Developer"

    def test_filter_vacancies_empty(self):
        """Тест фильтрации без ключевых слов"""
        filtered = filter_vacancies(self.sample_vacancies(), [])
        assert len(filtered) == 3

    def test_get_vacancies_by_salary(self):
        """Тест фильтрации по зарплате (диапазон)"""
        # Диапазон 85000-95000
        filtered = get_vacancies_by_salary(self.sample_vacancies(), "85000-95000")
        assert len(filtered) == 0

    def test_get_vacancies_by_salary_single_value(self):
        """Тест фильтрации по минимальной зарплате"""
        # Только минимальная зарплата 95000
        filtered = get_vacancies_by_salary(self.sample_vacancies(), "95000")
        assert len(filtered) == 2
        titles = [v.title for v in filtered]
        assert "Python Developer" in titles
        assert "JavaScript Developer" in titles
        assert "Java Developer" not in titles

    def test_get_vacancies_by_salary_no_range(self):
        """Тест фильтрации без диапазона зарплат"""
        filtered = get_vacancies_by_salary(self.sample_vacancies(), "")
        assert len(filtered) == 3

    def test_get_vacancies_by_salary_invalid_format(self):
        """Тест фильтрации с неверным форматом диапазона"""
        filtered = get_vacancies_by_salary(self.sample_vacancies(), "invalid-format")
        assert len(filtered) == 0

    def test_sort_vacancies(self):
        """Тест сортировки вакансий"""
        sorted_list = sort_vacancies(self.sample_vacancies())
        assert sorted_list[0].title == "Python Developer"
        assert sorted_list[0].avg_salary == 100000
        assert sorted_list[1].title == "JavaScript Developer"
        assert sorted_list[1].avg_salary == 100000
        assert sorted_list[2].title == "Java Developer"
        assert sorted_list[2].avg_salary == 80000

    def test_get_top_vacancies(self):
        """Тест получения топ N вакансий"""
        sorted_list = sort_vacancies(self.sample_vacancies())
        top_2 = get_top_vacancies(sorted_list, 2)
        assert len(top_2) == 2
        assert top_2[0].avg_salary == 100000
        assert top_2[1].avg_salary == 100000

    def test_get_top_vacancies_more_than_available(self):
        """Тест получения топ N вакансий, когда N больше доступных"""
        sorted_list = sort_vacancies(self.sample_vacancies())
        top_5 = get_top_vacancies(sorted_list, 5)
        assert len(top_5) == 3
