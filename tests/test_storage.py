import pytest
import os
import sys
import tempfile

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.vacancy import Vacancy  # noqa: E402
from src.storage.json_storage import JSONStorage  # noqa: E402


class TestJSONStorage:
    """Тесты для класса JSONStorage"""

    @pytest.fixture
    def storage(self):
        """Создание временного хранилища"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_filename = f.name
        storage = JSONStorage(temp_filename)
        yield storage
        # Очистка после теста
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)

    @pytest.fixture
    def sample_vacancy(self):
        """Создание тестовой вакансии"""
        return Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
        )

    def test_add_vacancy(self, storage, sample_vacancy):
        """Тест добавления вакансии"""
        storage.add_vacancy(sample_vacancy)

        vacancies = storage.get_vacancies()
        assert len(vacancies) == 1
        assert vacancies[0].title == "Python Developer"

    def test_duplicate_vacancy(self, storage, sample_vacancy):
        """Тест предотвращения дублирования"""
        storage.add_vacancy(sample_vacancy)
        storage.add_vacancy(sample_vacancy)  # Дубликат

        vacancies = storage.get_vacancies()
        assert len(vacancies) == 1

    def test_delete_vacancy(self, storage, sample_vacancy):
        """Тест удаления вакансии"""
        storage.add_vacancy(sample_vacancy)

        vacancies_before = storage.get_vacancies()
        assert len(vacancies_before) == 1

        storage.delete_vacancy(sample_vacancy)

        vacancies_after = storage.get_vacancies()
        assert len(vacancies_after) == 0

    def test_filter_by_keyword(self, storage, sample_vacancy):
        """Тест фильтрации по ключевому слову"""
        storage.add_vacancy(sample_vacancy)

        # Вакансия без ключевого слова
        vacancy2 = Vacancy(
            title="Java Developer",
            url="https://hh.ru/vacancy/456",
            description="Java programming",
        )
        storage.add_vacancy(vacancy2)

        vacancies = storage.get_vacancies(keyword="Python")
        assert len(vacancies) == 1
        assert vacancies[0].title == "Python Developer"

    def test_clear(self, storage, sample_vacancy):
        """Тест очистки хранилища"""
        storage.add_vacancy(sample_vacancy)
        storage.clear()

        vacancies = storage.get_vacancies()
        assert len(vacancies) == 0

    def test_filter_by_salary(self, storage, sample_vacancy):
        """Тест фильтрации по зарплате"""
        storage.add_vacancy(sample_vacancy)

        vacancies = storage.get_vacancies(salary_min=90000)
        assert len(vacancies) == 1
        assert vacancies[0].title == "Python Developer"

        vacancies = storage.get_vacancies(salary_min=200000)
        assert len(vacancies) == 0
