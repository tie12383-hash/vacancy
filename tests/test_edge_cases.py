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


class TestEdgeCases:
    """Тесты граничных случаев"""

    def test_filter_with_empty_words(self):
        """Тест фильтрации с пустыми ключевыми словами"""
        vacancies = [
            Vacancy("Python", "http://test.com", salary_from=100000),
            Vacancy("Java", "http://test.com", salary_from=90000),
        ]

        # Пустой список слов
        result = filter_vacancies(vacancies, [])
        assert len(result) == 2

        # Слова с пробелами
        result = filter_vacancies(vacancies, [" ", ""])
        assert len(result) == 2

    def test_filter_case_insensitive(self):
        """Тест фильтрации без учета регистра"""
        vacancies = [
            Vacancy(
                title="Python Developer",
                url="http://test.com",
                salary_from=100000,
                description="PYTHON programming",
            )
        ]

        # Разный регистр
        result = filter_vacancies(vacancies, ["python"])
        assert len(result) == 1

        result = filter_vacancies(vacancies, ["PYTHON"])
        assert len(result) == 1

        result = filter_vacancies(vacancies, ["Python"])
        assert len(result) == 1

    def test_salary_range_variations(self):
        """Тест различных форматов диапазона зарплат"""
        vacancies = [
            Vacancy("Test", "http://test.com", salary_from=100000, salary_to=150000)
        ]

        # Стандартный формат
        result = get_vacancies_by_salary(vacancies, "90000-130000")
        assert len(result) == 1

        # Только минимальная зарплата
        result = get_vacancies_by_salary(vacancies, "90000")
        assert len(result) == 1

        # Пробелы в диапазоне
        result = get_vacancies_by_salary(vacancies, " 90000 - 130000 ")
        assert len(result) == 1

        # Неверный формат (буквы) - по новой логике возвращаем пустой список
        result = get_vacancies_by_salary(vacancies, "invalid")
        assert len(result) == 0

        # Пустая строка
        result = get_vacancies_by_salary(vacancies, "")
        assert len(result) == 1

        # Пробелы
        result = get_vacancies_by_salary(vacancies, "   ")
        assert len(result) == 1

    def test_salary_range_invalid(self):
        """Тест неверных диапазонов зарплат"""
        vacancies = [
            Vacancy("Test", "http://test.com", salary_from=100000, salary_to=150000)
        ]

        # Минимальная больше максимальной - должно поменяться местами
        result = get_vacancies_by_salary(vacancies, "200000-100000")
        assert len(result) == 1

        # Отрицательные значения с форматом -100-100
        result = get_vacancies_by_salary(vacancies, "-100-100")
        assert len(result) == 0

        # Несколько дефисов
        result = get_vacancies_by_salary(vacancies, "100-200-300")
        assert len(result) == 0

    def test_negative_salary_range(self):
        """Тест отрицательного диапазона зарплат"""
        vacancies = [
            Vacancy("Test", "http://test.com", salary_from=50000, salary_to=70000)
        ]

        # Отрицательные числа в диапазоне
        result = get_vacancies_by_salary(vacancies, "-100--50")
        assert len(result) == 0

        # Положительный диапазон, но вакансия не входит
        result = get_vacancies_by_salary(vacancies, "100000-200000")
        assert len(result) == 0

    def test_sort_empty_list(self):
        """Тест сортировки пустого списка"""
        result = sort_vacancies([])
        assert len(result) == 0

    def test_sort_vacancies_without_salary(self):
        """Тест сортировки вакансий без зарплаты"""
        vacancies = [
            Vacancy("No Salary 1", "http://test.com"),
            Vacancy("No Salary 2", "http://test.com"),
            Vacancy("With Salary", "http://test.com", salary_from=100000),
        ]

        sorted_list = sort_vacancies(vacancies)

        # Вакансия с зарплатой должна быть первой
        assert sorted_list[0].title == "With Salary"
        # Затем вакансии без зарплаты
        assert sorted_list[1].title == "No Salary 1"
        assert sorted_list[2].title == "No Salary 2"

    def test_top_vacancies_edge_cases(self):
        """Тест граничных случаев для топ N вакансий"""
        vacancies = [
            Vacancy("Vacancy 1", "http://test.com", salary_from=100000),
            Vacancy("Vacancy 2", "http://test.com", salary_from=90000),
        ]

        # N = 0
        result = get_top_vacancies(vacancies, 0)
        assert len(result) == 0

        # N = 1
        result = get_top_vacancies(vacancies, 1)
        assert len(result) == 1

        # N больше чем вакансий
        result = get_top_vacancies(vacancies, 5)
        assert len(result) == 2

        # Отрицательное N
        result = get_top_vacancies(vacancies, -1)
        assert len(result) == 0

        # Пустой список
        result = get_top_vacancies([], 5)
        assert len(result) == 0
