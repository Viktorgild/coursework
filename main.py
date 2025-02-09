from datetime import datetime

import pandas as pd

from src.logging_config import setup_logger
from src.reports import generate_report
from src.services import analyze_cashback, read_json_file
from src.utils import get_exchange_rates, get_transactions
from src.views import calculate_card_details, top_transactions, greetings

# Настройка логирования
logger = setup_logger("main_logger", "../logs/main.log")
logger.info(greetings)
# Пример данных транзакций
transactions = [
    {"card_number": "1234567890123456", "amount": 1000, "date": "2023-10-01", "time": "12:00"},
    {"card_number": "1234567890123456", "amount": 500, "date": "2023-10-02", "time": "14:00"},
    {"card_number": "9876543210987654", "amount": 2000, "date": "2023-10-03", "time": "15:00"},
    {"card_number": "9876543210987654", "amount": 1500, "date": "2023-10-04", "time": "16:00"},
    {"card_number": "1234567890123456", "amount": 750, "date": "2023-10-05", "time": "17:00"},
]

# Вычисляем детали карт
logger.info("Начинаем вычисление деталей карт.")
card_details = calculate_card_details(transactions)

# Выводим детали карт
logger.info("Детали карт успешно вычислены.")
logger.info("Детали карт: %s", card_details)

# Получаем топ-5 транзакций
logger.info("Получаем топ-5 транзакций.")
top_transactions(card_details)

data = {
    "transactions": [
        {"category": "Категория 1", "cashback": 500, "date": datetime(2023, 1, 1)},
        {"category": "Категория 2", "cashback": 1000, "date": datetime(2023, 2, 1)},
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
user_settings = read_json_file("../user_settings.json")
rates = get_transactions(user_settings)

# Использование полученных данных
logger.info("Полученные данные транзакций: %s", rates)
logger.info(rates)

# Вызов функции для получения обменных курсов
logger.info("Получаем обменные курсы.")
exchange_rates = get_exchange_rates(user_settings)
logger.info(exchange_rates)

logger.info("Функция top_transactions успешно выполнена.")

# Чтение данных из Excel
logger.info("Чтение данных из Excel.")
df = pd.read_excel("../data/operations.xlsx")
df.set_index("Категория", drop=False, inplace=True)
df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

# Пример использования функции
data = "2021-12-31"
category = "Супермаркеты"
logger.info("Генерация отчета для категории: %s за дату: %s", category, data)
result = generate_report(df, category, data)

# Вывод результата
logger.info("Результат генерации отчета: %s", result)
