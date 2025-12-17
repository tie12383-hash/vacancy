from __future__ import annotations
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = (
        "_title",
        "_url",
        "_salary_from",
        "_salary_to",
        "_currency",
        "_description",
        "_requirements",
        "_company",
    )

    def __init__(
        self,
        title: str,
        url: str,
        salary_from: Optional[int] = None,
        salary_to: Optional[int] = None,
        currency: str = "RUR",
        description: str = "",
        requirements: str = "",
        company: str = "",
    ):

        self._title = self._validate_title(title)
        self._url = self._validate_url(url)
        self._salary_from = self._validate_salary(salary_from)
        self._salary_to = self._validate_salary(salary_to)
        self._currency = self._validate_currency(currency)
        self._description = description
        self._requirements = requirements
        self._company = company

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary_from(self) -> Optional[int]:
        return self._salary_from

    @property
    def salary_to(self) -> Optional[int]:
        return self._salary_to

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def description(self) -> str:
        return self._description

    @property
    def requirements(self) -> str:
        return self._requirements

    @property
    def company(self) -> str:
        return self._company

    @property
    def avg_salary(self) -> float:
        """Рассчитывает среднюю зарплату"""
        if self._salary_from and self._salary_to:
            return (self._salary_from + self._salary_to) / 2
        elif self._salary_from:
            return float(self._salary_from)
        elif self._salary_to:
            return float(self._salary_to)
        return 0.0

    def _validate_title(self, title: str) -> str:
        """Валидация названия вакансии"""
        if not title or not isinstance(title, str):
            raise ValueError("Название вакансии обязательно и должно быть строкой")
        return title.strip()

    def _validate_url(self, url: str) -> str:
        """Валидация URL"""
        if not url or not isinstance(url, str):
            raise ValueError("URL обязателен и должен быть строкой")
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL должен начинаться с http:// или https://")
        return url

    def _validate_salary(self, salary: Optional[int]) -> Optional[int]:
        """Валидация зарплаты"""
        if salary is not None:
            if not isinstance(salary, (int, float)):
                raise ValueError("Зарплата должна быть числом")
            if salary < 0:
                raise ValueError("Зарплата не может быть отрицательной")
            return int(salary)
        return None

    def _validate_currency(self, currency: str) -> str:
        """Валидация валюты"""
        if not isinstance(currency, str):
            raise ValueError("Валюта должна быть строкой")
        return currency.upper()

    def __str__(self) -> str:
        salary_info = self.get_salary_display()
        return (
            f"{self._title} | {self._company}\n"
            f"Зарплата: {salary_info}\n"
            f"Требования: {self._requirements[:100]}...\n"
            f"Ссылка: {self._url}"
        )

    def get_salary_display(self) -> str:
        """Возвращает отформатированную информацию о зарплате"""
        if self._salary_from and self._salary_to:
            return f"{self._salary_from:,} - {self._salary_to:,} {self._currency}"
        elif self._salary_from:
            return f"от {self._salary_from:,} {self._currency}"
        elif self._salary_to:
            return f"до {self._salary_to:,} {self._currency}"
        else:
            return "Зарплата не указана"

    # Методы сравнения
    def __lt__(self, other: Vacancy) -> bool:
        return self.avg_salary < other.avg_salary

    def __le__(self, other: Vacancy) -> bool:
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other: Vacancy) -> bool:
        return self.avg_salary > other.avg_salary

    def __ge__(self, other: Vacancy) -> bool:
        return self.avg_salary >= other.avg_salary

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def to_dict(self) -> Dict[str, Any]:
        """Конвертирует вакансию в словарь"""
        return {
            "title": self._title,
            "url": self._url,
            "salary_from": self._salary_from,
            "salary_to": self._salary_to,
            "currency": self._currency,
            "description": self._description,
            "requirements": self._requirements,
            "company": self._company,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Vacancy:
        """Создает вакансию из словаря"""
        return cls(
            title=data.get("title", ""),
            url=data.get("url", ""),
            salary_from=data.get("salary_from"),
            salary_to=data.get("salary_to"),
            currency=data.get("currency", "RUR"),
            description=data.get("description", ""),
            requirements=data.get("requirements", ""),
            company=data.get("company", ""),
        )

    @classmethod
    def cast_to_object_list(cls, hh_data: List[Dict[str, Any]]) -> List[Vacancy]:
        """Конвертирует данные из HH API в список объектов Vacancy"""
        vacancies = []
        for item in hh_data:
            # Парсим зарплату
            salary_data = item.get("salary")
            salary_from = salary_to = None
            currency = "RUR"

            if salary_data:
                salary_from = salary_data.get("from")
                salary_to = salary_data.get("to")
                currency = salary_data.get("currency", "RUR")

            # Создаем объект Vacancy
            vacancy = cls(
                title=item.get("name", ""),
                url=item.get("alternate_url", ""),
                salary_from=salary_from,
                salary_to=salary_to,
                currency=currency,
                description=(
                    item.get("description", "")[:500] if item.get("description") else ""
                ),
                requirements=item.get("snippet", {}).get("requirement", ""),
                company=item.get("employer", {}).get("name", ""),
            )
            vacancies.append(vacancy)

        return vacancies
