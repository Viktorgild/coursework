from datetime import datetime
import pandas as pd
import json

from src.logging_config import setup_logger
from src.reports import generate_report
from src.services import analyze_cashback, read_json_file
from src.utils import get_exchange_rates, get_transactions
from src.views import calculate_card_details, top_transactions, greetings, get_data_by_date, get_summary_data

# Настройка логирования
logger = setup_logger("main_logger", "../logs/main.log")

def main():
    logger.info(greetings())  # Вызываем функцию, а не передаем ссылку

    # Пример данных транзакций
    transactions = [
        {"card_number": "1234567890123456", "amount": 1000, "date": "2023-10-01", "time": "12:00"},
        {"card_number": "1234567890123456", "amount": 500, "date": "2023-10-02", "time": "14:00"},
        {"card_number": "9876543210987654", "amount": 2000, "date": "2023-10-03", "time": "15:00"},
        {"card_number": "9876543210987654", "amount": 1500, "date": "2023-10-04", "time": "16:00"},
        {"card_number": "1234567890123456", "amount": 750, "date": "2023-10-05", "time": "17:00"},
    ]


    date_str = "31.12.2021"  # Тестовая дата для примера
    logger.info("Запрашиваем данные за дату: %s", date_str)
    summary_data = get_summary_data(date_str)
    logger.info("JSON-ответ: %s", json.dumps(summary_data, ensure_ascii=False, indent=4))

    # Вычисляем детали карт
    logger.info("Начинаем вычисление деталей карт.")
    card_details = calculate_card_details(transactions)

    # Выводим детали карт
    logger.info("Детали карт успешно вычислены.")
    logger.info("Детали карт: %s", card_details)

    # Получаем топ-5 транзакций
    logger.info("Получаем топ-5 транзакций.")
    top_transactions(card_details)

    # Данные для анализа кэшбэка
    data = {
        "transactions": [
            {"category": "Категория 1", "cashback": 500, "date": "2023-01-01"},
            {"category": "Категория 2", "cashback": 1000, "date": "2023-02-01"},
        ],
        "categories": ["Категория 1", "Категория 2"],
    }

    # Вызов функции
    logger.info("Анализируем кэшбэк.")
    result = analyze_cashback(data, 2023, 2)

    # Вывод результата
    logger.info("Результат анализа кэшбэка: %s", result)

    # Чтение настроек пользователя из JSON
    logger.info("Чтение настроек пользователя из JSON.")
    user_settings = read_json_file("./user_settings.json")
    rates = get_transactions(user_settings)

    # Использование полученных данных
    logger.info("Полученные данные транзакций: %s", rates)

    # Вызов функции для получения обменных курсов
    logger.info("Получаем обменные курсы.")
    exchange_rates = get_exchange_rates(user_settings)
    logger.info("Курсы валют: %s", exchange_rates)

    # Чтение данных из Excel
    logger.info("Чтение данных из Excel.")
    df = pd.read_excel("./data/operations.xlsx")
    df.set_index("Категория", drop=False, inplace=True)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    # Генерация отчета
    formatted_date = datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
    category = "Супермаркеты"
    logger.info("Генерация отчета для категории: %s за дату: %s", category, formatted_date)
    result = generate_report(df, category, formatted_date)

    # Вывод результата
    logger.info("Результат генерации отчета: %s", result)

    # Вызов функции получения данных по дате (по ТЗ)
    logger.info("Получаем данные за дату: %s", date_str)
    transactions_by_date = get_data_by_date(date_str)
    logger.info("Транзакции за %s: %s", date_str, transactions_by_date)


if __name__ == "__main__":
    main()