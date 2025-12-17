import requests
import time
import random
from typing import Dict, List, Any
from ..api.abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self._base_url = "https://api.hh.ru"
        # Правильные заголовки для HH API
        self._headers = {
            "User-Agent": "MyApp/1.0 (myemail@example.com)",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _connect(self) -> None:
        """
        Упрощенная проверка подключения
        """
        try:
            # Простой запрос для проверки доступности
            response = requests.get(
                f"{self._base_url}/", headers=self._headers, timeout=10
            )

            if response.status_code != 200:
                print(f"Предупреждение: API HH.ru вернул статус {response.status_code}")
            else:
                print("Подключение к API HH.ru успешно")

        except requests.exceptions.RequestException as e:
            print(f"Предупреждение: Ошибка подключения к API HH.ru: {e}")

    def get_vacancies(
        self, search_query: str, per_page: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Получение вакансий с HH.ru с правильными параметрами

        Args:
            search_query: Поисковый запрос
            per_page: Количество вакансий на странице (макс 100)

        Returns:
            Список словарей с данными о вакансиях
        """
        # Подключаемся перед запросом
        self._connect()

        # Правильные параметры для HH API
        params = {
            "text": search_query,
            "area": 113,  # Россия
            "per_page": min(per_page, 50),
            "page": 0,
            "search_field": "name",
            "order_by": "relevance",
            "only_with_salary": False,
        }

        # Добавляем небольшую случайную задержку
        time.sleep(random.uniform(0.5, 1.5))

        try:
            print(f"Отправка запроса к API HH.ru: {search_query}")

            response = requests.get(
                f"{self._base_url}/vacancies",
                headers=self._headers,
                params=params,
                timeout=30,
            )

            print(f"Статус ответа: {response.status_code}")

            if response.status_code == 400:
                # Пробуем без некоторых параметров
                print("Попытка альтернативного запроса...")
                simple_params = {"text": search_query, "area": 113, "per_page": 20}

                response = requests.get(
                    f"{self._base_url}/vacancies",
                    headers=self._headers,
                    params=simple_params,
                    timeout=30,
                )
                print(f"Статус альтернативного ответа: {response.status_code}")

            # Проверяем успешность запроса
            if response.status_code != 200:
                print(f"Ошибка API: {response.status_code}")
                print(f"Ответ сервера: {response.text[:500]}")
                return []

            data = response.json()

            # Проверяем структуру ответа
            if "items" not in data:
                print("Неожиданная структура ответа API")
                print(f"Ключи в ответе: {list(data.keys())}")
                return []

            items = data.get("items", [])
            print(f"Получено вакансий: {len(items)}")

            # Если нет вакансий, но есть suggestions
            if not items and "suggestions" in data:
                print("Используем suggestions...")
                items = data.get("suggestions", [])

            return items

        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети: {e}")
            return []
        except Exception as e:
            print(f"Общая ошибка: {e}")
            return []
