import pytest
from unittest.mock import patch, Mock
import sys
import os

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.api.hh_api import HeadHunterAPI  # noqa: E402


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    @pytest.fixture
    def api_instance(self):
        return HeadHunterAPI()

    def test_init(self, api_instance):
        """Тест инициализации"""
        assert api_instance._base_url == "https://api.hh.ru"
        assert "User-Agent" in api_instance._headers

    @patch("requests.get")
    def test_connect_success(self, mock_get, api_instance):
        """Тест успешного подключения"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "OK"
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        # Переподключаемся
        api_instance._connect()
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get, api_instance):
        """Тест успешного получения вакансий"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"name": "Python Developer", "id": "123"},
                {"name": "Java Developer", "id": "456"},
            ]
        }
        mock_get.return_value = mock_response

        vacancies = api_instance.get_vacancies("Python")

        assert len(vacancies) == 2
        assert vacancies[0]["name"] == "Python Developer"

    @patch("requests.get")
    def test_get_vacancies_empty(self, mock_get, api_instance):
        """Тест получения пустого списка вакансий"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        vacancies = api_instance.get_vacancies("NonExistentQuery")

        assert len(vacancies) == 0
