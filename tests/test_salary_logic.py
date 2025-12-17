import sys
import os

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.vacancy import Vacancy  # noqa: E402
from src.utils.helpers import get_vacancies_by_salary  # noqa: E402


def test_salary_logic():
    """Тест логики фильтрации по зарплате"""
    vacancies = [
        Vacancy("Вакансия 1", "http://test.com", salary_from=100000, salary_to=150000),
        Vacancy("Вакансия 2", "http://test.com", salary_from=80000, salary_to=120000),
        Vacancy("Вакансия 3", "http://test.com", salary_from=90000),
        Vacancy("Вакансия 4", "http://test.com"),
    ]

    # Тест 1: Диапазон 90000-110000
    result = get_vacancies_by_salary(vacancies, "90000-110000")
    assert len(result) == 2

    # Тест 2: Только минимальная зарплата 95000
    result = get_vacancies_by_salary(vacancies, "95000")
    assert len(result) == 2

    # Тест 3: Диапазон 200000-300000
    result = get_vacancies_by_salary(vacancies, "200000-300000")
    assert len(result) == 0

    # Тест 4: Отрицательные значения "-100-100"
    result = get_vacancies_by_salary(vacancies, "-100-100")
    assert len(result) == 0

    # Тест 5: Пустая строка
    result = get_vacancies_by_salary(vacancies, "")
    assert len(result) == 4

    print("Все тесты логики зарплат пройдены!")


if __name__ == "__main__":
    test_salary_logic()
