from typing import List
from ..models.vacancy import Vacancy


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевым словам

    Args:
        vacancies: Список вакансий
        filter_words: Список ключевых слов

    Returns:
        Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    # Очищаем ключевые слова от пустых строк и пробелов
    clean_words = [word.strip().lower() for word in filter_words if word.strip()]
    if not clean_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        # Объединяем все текстовые поля для поиска
        vacancy_text = (
            f"{vacancy.title} {vacancy.description} "
            f"{vacancy.requirements} {vacancy.company}"
        ).lower()

        # Проверяем, содержатся ли все ключевые слова
        if all(word in vacancy_text for word in clean_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат

    Args:
        vacancies: Список вакансий
        salary_range: Диапазон зарплат в формате "100000-150000" или "100000"

    Returns:
        Отфильтрованный список вакансий

    Логика:
    - Пустая строка или пробелы: возвращаем все вакансии
    - Одно число: минимальная зарплата
    - Два числа через дефис: диапазон зарплат
    - Любой другой формат: пустой список
    """
    # Если строка пустая или состоит только из пробелов, возвращаем все вакансии
    if not salary_range or salary_range.isspace():
        return vacancies

    # Удаляем лишние пробелы
    salary_range = salary_range.strip()

    try:
        if "-" in salary_range:
            # Разделяем на части
            parts = [part.strip() for part in salary_range.split("-")]

            # Должно быть ровно 2 непустые части
            if len(parts) != 2 or not parts[0] or not parts[1]:
                return []

            min_salary = int(parts[0])
            max_salary = int(parts[1])

            # Если min > max, меняем местами
            if min_salary > max_salary:
                min_salary, max_salary = max_salary, min_salary

        else:
            # Одно число
            min_salary = int(salary_range)
            max_salary = float("inf")

    except ValueError:
        # Ошибка преобразования в число
        return []

    # Фильтрация вакансий
    filtered = []
    for vacancy in vacancies:
        avg_salary = vacancy.avg_salary
        # Проверяем, что вакансия имеет зарплату и она попадает в диапазон
        if avg_salary > 0 and min_salary <= avg_salary <= max_salary:
            filtered.append(vacancy)

    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортирует вакансии по убыванию зарплаты

    Args:
        vacancies: Список вакансий

    Returns:
        Отсортированный список вакансий
    """
    # Сначала фильтруем вакансии без зарплаты
    vacancies_with_salary = [v for v in vacancies if v.avg_salary > 0]
    vacancies_without_salary = [v for v in vacancies if v.avg_salary == 0]

    # Сортируем вакансии с зарплатой
    sorted_with_salary = sorted(
        vacancies_with_salary, key=lambda v: v.avg_salary, reverse=True
    )

    # Возвращаем отсортированные вакансии с зарплатой, затем без зарплаты
    return sorted_with_salary + vacancies_without_salary


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий

    Args:
        vacancies: Список вакансий
        top_n: Количество вакансий для возврата

    Returns:
        Список топ N вакансий
    """
    if top_n <= 0:
        return []

    return vacancies[: min(top_n, len(vacancies))]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Выводит вакансии в читаемом формате

    Args:
        vacancies: Список вакансий для вывода
    """
    if not vacancies:
        print("Вакансии не найдены")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{'='*60}")
        print(f"Вакансия #{i}")
        print(f"{'='*60}")
        print(vacancy)
        print()
