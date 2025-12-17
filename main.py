"""
Точка входа в приложение
"""
import os
import sys
import traceback

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.api.hh_api import HeadHunterAPI
from src.api.fallback_hh_api import FallbackHeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage
from src.utils.helpers import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies,
)


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем"""
    print("=" * 60)
    print("ПОИСК ВАКАНСИЙ НА HH.RU")
    print("=" * 60)

    try:
        # Запрос параметров поиска
        search_query = input(
            "\nВведите поисковый запрос (например: Python разработчик): "
        ).strip()

        if not search_query:
            print("Поисковый запрос не может быть пустым!")
            return

        # Получение вакансий
        print(f"\nИщу вакансии по запросу: '{search_query}'...")

        hh_vacancies_data = []

        # Сначала пробуем основной API
        try:
            print("Попытка 1: Основной API...")
            hh_api = HeadHunterAPI()
            hh_vacancies_data = hh_api.get_vacancies(search_query, per_page=20)
        except Exception as e:
            print(f"Основной API не сработал: {e}")
            hh_vacancies_data = []

        # Если основной не сработал, пробуем резервный
        if not hh_vacancies_data:
            print("Попытка 2: Резервный API...")
            try:
                fallback_api = FallbackHeadHunterAPI()
                hh_vacancies_data = fallback_api.get_vacancies(
                    search_query, per_page=15
                )
            except Exception as e:
                print(f"Резервный API не сработал: {e}")

        # Если API не работают, используем тестовые данные
        if not hh_vacancies_data:
            print("\nAPI не доступен. Использую тестовые данные...")
            hh_vacancies_data = load_sample_vacancies()
            for item in hh_vacancies_data:
                if search_query.lower() not in item["name"].lower():
                    item["name"] = f"{search_query} - {item['name']}"

        # Конвертация в объекты
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_data)
        print(f"\nНайдено вакансий: {len(vacancies_list)}")

        if not vacancies_list:
            print("Нет вакансий для обработки")
            return

        # Сохранение в файл
        json_saver = JSONStorage()
        for vacancy in vacancies_list:
            json_saver.add_vacancy(vacancy)
        print("Вакансии сохранены в файл: data/vacancies.json")

        # Основной цикл взаимодействия
        while True:
            print("\n" + "=" * 60)
            print("ОСНОВНОЕ МЕНЮ")
            print("1. Вывести топ N вакансий по зарплате")
            print("2. Найти вакансии по ключевому слову в описании")
            print("3. Фильтровать по диапазону зарплат")
            print("4. Вывести все вакансии")
            print("5. Поиск вакансий другой специальности")
            print("6. Выход")

            choice = input("\nВыберите действие (1-6): ").strip()

            if choice == "1":
                try:
                    top_n = int(
                        input("Введите количество вакансий для вывода (топ N): ")
                    )
                    if top_n <= 0:
                        print("Число должно быть положительным!")
                        continue

                    # Сортируем только вакансии с указанной зарплатой
                    vacancies_with_salary = [
                        v for v in vacancies_list if v.avg_salary > 0
                    ]
                    if not vacancies_with_salary:
                        print("Нет вакансий с указанной зарплатой для сортировки")
                        continue

                    sorted_vacancies = sort_vacancies(vacancies_with_salary)
                    top_vacancies = get_top_vacancies(
                        sorted_vacancies, min(top_n, len(sorted_vacancies))
                    )
                    print(f"\nТоп {len(top_vacancies)} вакансий по зарплате:")
                    print_vacancies(top_vacancies)
                except ValueError:
                    print("Введите корректное число!")

            elif choice == "2":
                keyword = input(
                    "Введите ключевое слово для поиска в описании: "
                ).strip()
                if keyword:
                    filtered = filter_vacancies(vacancies_list, [keyword])
                    print(
                        f"\nНайдено вакансий с ключевым словом '{keyword}': "
                        f"{len(filtered)}"
                    )
                    if filtered:
                        print_vacancies(filtered)
                else:
                    print("Ключевое слово не может быть пустым!")

            elif choice == "3":
                salary_range = input(
                    "Введите диапазон зарплат (например: 100000-200000): "
                ).strip()
                if salary_range:
                    filtered = get_vacancies_by_salary(vacancies_list, salary_range)
                    print(f"\nНайдено вакансий в указанном диапазоне: {len(filtered)}")
                    if filtered:
                        print_vacancies(filtered)
                else:
                    print("Диапазон зарплат не может быть пустым!")

            elif choice == "4":
                print(f"\nВсе вакансии ({len(vacancies_list)}):")
                print_vacancies(vacancies_list)

            elif choice == "5":
                # Выход в главное меню
                print("\nВозврат к поиску...")
                break

            elif choice == "6":
                print("До свидания!")
                sys.exit(0)

            else:
                print("Неверный выбор. Попробуйте еще раз.")

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
        sys.exit(0)
    except Exception as e:  # noqa: BLE001
        print(f"\nПроизошла ошибка: {e}")
        traceback.print_exc()
        print("Пожалуйста, попробуйте снова")


def load_sample_vacancies() -> list:
    """Загрузка тестовых данных из файла, если API не работает"""
    import json
    import os

    sample_file = "data/sample_vacancies.json"

    if os.path.exists(sample_file):
        try:
            with open(sample_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    # Создаем тестовые данные
    sample_data = [
        {
            "name": "Python разработчик",
            "alternate_url": "https://hh.ru/vacancy/12345678",
            "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
            "description": "Разработка backend на Python. Опыт от 2 лет.",
            "snippet": {"requirement": "Python, Django, Flask, PostgreSQL"},
            "employer": {"name": "IT компания"},
        },
        {
            "name": "Senior Python Developer",
            "alternate_url": "https://hh.ru/vacancy/87654321",
            "salary": {"from": 200000, "to": 300000, "currency": "RUR"},
            "description": "Разработка высоконагруженных систем.",
            "snippet": {"requirement": "Python, asyncio, Redis, Docker"},
            "employer": {"name": "Технологический стартап"},
        },
        {
            "name": "Python Data Engineer",
            "alternate_url": "https://hh.ru/vacancy/11223344",
            "salary": {"from": 150000, "to": 220000, "currency": "RUR"},
            "description": "Работа с большими данными и ETL процессами.",
            "snippet": {"requirement": "Python, SQL, Airflow, PySpark"},
            "employer": {"name": "Data компания"},
        },
    ]

    # Сохраняем тестовые данные
    os.makedirs("data", exist_ok=True)
    with open(sample_file, "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)

    return sample_data


if __name__ == "__main__":
    # Создаем директории, если их нет
    os.makedirs("data", exist_ok=True)

    # Основной цикл программы
    while True:
        user_interaction()

        cont = input("\nХотите выполнить новый поиск? (да/нет): ").strip().lower()
        if cont not in ["да", "yes", "y", "д"]:
            print("Выход из программы...")
            break
