import datetime
import pandas as pd
from src.logging_config import setup_logger
from src.utils import get_exchange_rates, get_transactions

# Настройка логгера
logger = setup_logger("views_logger", "../logs/views.log")


def greetings() -> str:
    """Функция, которая возвращает строку с приветствием в зависимости от времени."""
    try:
        hour = int(datetime.datetime.now().strftime("%H"))
        if 6 <= hour <= 12:
            return "Доброе утро"
        elif 13 <= hour <= 17:
            return "Добрый день"
        elif 18 <= hour <= 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"
    except Exception as e:
        logger.error(f"Ошибка в функции greetings: {e}")
        return "Ошибка определения приветствия"


def calculate_card_details(transactions):
    """
    Функция для расчёта последних 4 цифр номера карты, общей суммы расходов и кешбэка для каждой карты.

    :param transactions: список транзакций
    :return: словарь с деталями по каждой карте
    """
    card_details = {}

    for transaction in transactions:
        try:
            card_number = transaction["card_number"]
            last_four_digits = card_number[-4:]

            if last_four_digits not in card_details:
                card_details[last_four_digits] = {
                    "last_four_digits": last_four_digits,
                    "total_amount": 0,
                    "cashback": 0,
                    "transactions": [],
                }

            card_details[last_four_digits]["total_amount"] += transaction["amount"]
            card_details[last_four_digits]["cashback"] = card_details[last_four_digits]["total_amount"] // 100
            card_details[last_four_digits]["transactions"].append(transaction)

        except KeyError as e:
            logger.error(f"Ошибка: отсутствует ключ {e} в транзакции.")
        except Exception as e:
            logger.exception(f"Ошибка обработки транзакции {transaction}: {e}")

    return card_details


def top_transactions(card_details):
    """
    Функция для вывода топ-5 транзакций по каждой карте.

    :param card_details: словарь с деталями по каждой карте
    """
    for last_four_digits, details in card_details.items():
        try:
            sorted_transactions = sorted(details["transactions"], key=lambda x: x["amount"], reverse=True)
            logger.info(f"Топ-5 транзакций для карты {last_four_digits}:")
            for i, transaction in enumerate(sorted_transactions[:5]):
                logger.info(
                    f"{i + 1}: Дата: {transaction['date']}, Время: {transaction['time']}, Сумма: {transaction['amount']} рублей"
                )
        except Exception as e:
            logger.error(f"Ошибка при обработке транзакций для карты {last_four_digits}: {e}")


def get_data_by_date(date_str: str):
    """Возвращает транзакции за указанную дату из Excel-файла."""
    try:
        date_obj = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
        df = pd.read_excel("./data/operations.xlsx")
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

        filtered_transactions = df[df["Дата операции"].dt.date == date_obj]
        return filtered_transactions.to_dict(orient="records")

    except ValueError:
        logger.error(f"Неверный формат даты: {date_str}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при обработке даты {date_str}: {e}")

        return []
def get_summary_data(date_str: str):
    """Собирает все данные и возвращает JSON-ответ."""
    transactions = get_data_by_date(date_str)
    card_details = calculate_card_details(transactions)
    top_trans = top_transactions(card_details)

    # Читаем настройки пользователя
    user_settings = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }

    exchange_rates = get_exchange_rates(user_settings)
    stock_prices = get_transactions(user_settings)

    return {
        "greeting": greetings(),
        "cards": card_details,
        "top_transactions": top_trans,
        "exchange_rates": exchange_rates,
        "stock_prices": stock_prices
    }