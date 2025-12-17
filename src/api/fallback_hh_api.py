from typing import Dict, List, Any
from .abstract_api import AbstractAPI


class FallbackHeadHunterAPI(AbstractAPI):
    """
    Резервный класс для работы с HH.ru через альтернативный метод
    Использует более простые запросы
    """

    def __init__(self):
        self._base_url = "https://api.hh.ru"
        # Более простые заголовки
        self._headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }

    def _connect(self) -> None:
        """Простая проверка подключения"""
        print("Используется резервный метод подключения...")

    def get_vacancies(
        self, search_query: str, per_page: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Упрощенный метод получения вакансий
        """
        # Пробуем несколько разных форматов запросов
        endpoints_to_try = [
            {
                "url": f"{self._base_url}/vacancies",
                "params": {"text": search_query, "area": 113, "per_page": per_page},
            },
            {
                "url": f"{self._base_url}/vacancies",
                "params": {
                    "text": f'"{search_query}"',
                    "area": 1,
                    "per_page": per_page,
                },
            },
        ]

        for endpoint in endpoints_to_try:
            try:
                import requests
                import time

                time.sleep(1)

                response = requests.get(
                    endpoint["url"],
                    headers=self._headers,
                    params=endpoint["params"],
                    timeout=30,
                )

                if response.status_code == 200:
                    data = response.json()
                    return data.get("items", [])

            except Exception as e:
                print(f"Ошибка в альтернативном методе: {e}")
                continue

        return []
