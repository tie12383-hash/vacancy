from abc import ABC, abstractmethod
from typing import List
from ..models.vacancy import Vacancy


class AbstractStorage(ABC):
    """Абстрактный класс для работы с хранилищем данных"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в хранилище"""
        pass

    @abstractmethod
    def get_vacancies(self, **kwargs) -> List[Vacancy]:
        """
        Получает вакансии из хранилища по критериям

        Args:
            **kwargs: Критерии фильтрации

        Returns:
            Список вакансий
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из хранилища"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очищает хранилище"""
        pass
