from abc import ABC, abstractmethod
from typing import Dict, List, Any


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def _connect(self) -> None:
        """
        Подключение к API сервиса
        Raises:
            ConnectionError: если не удалось подключиться
        """
        pass

    @abstractmethod
    def get_vacancies(
        self, search_query: str, per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Получение вакансий по поисковому запросу

        Args:
            search_query: Поисковый запрос
            per_page: Количество вакансий на странице

        Returns:
            Список словарей с данными о вакансиях
        """
        pass
