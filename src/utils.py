import json
import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
from src.logging_config import setup_logger

# Настройка логгера
logger = setup_logger("utils_logger", "../logs/utils.log")

def read_json_file(filename):
    """Функция для чтения файла JSON."""
    with open(filename, "r") as file:
        data = json.load(file)
    return data

def get_transactions(data):
    """Функция для получения текущего курса валют."""
    symbols_list = data["user_currencies"]
    result_dict = {}

    for i, symbol in enumerate(symbols_list):
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={symbol}&from={symbols_list[(i + 1) % len(symbols_list)]}&amount=1"
        headers = {"apikey": os.getenv("API_KEY")}

        logger.debug("Начало запроса для символа: %s", symbol)

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                result = response.json()  # Изменено на json() для получения данных
                logger.info("Успешный запрос для символа: %s", symbol)
                result_dict[symbol] = result
            else:
                logger.error("Ошибка запроса для символа %s: %s", symbol, response.text)

        except Exception as e:
            logger.exception("Произошла ошибка при запросе для символа %s: %s", symbol, e)

    return result_dict

load_dotenv()

def get_exchange_rates(symbol_or_data):
    """Функция для получения курсов акций за последний месяц."""
    api = os.getenv("API_KEY")  # Убедитесь, что переменная окружения правильная
    logger.debug("Начало запроса для получения курсов акций")

    try:
        if isinstance(symbol_or_data, dict):
            result_dict = {}
            for symbol in symbol_or_data["user_stocks"]:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api}"
                r = requests.get(url)
                data = r.json()
                result_dict[symbol] = filter_last_month_data(data)
            return result_dict
        else:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol_or_data}&apikey={api}"
            r = requests.get(url)
            data = r.json()
            return {symbol_or_data: filter_last_month_data(data)}
    except Exception as e:
        logger.error("Произошла ошибка: %s", e)
        return None  # Возвращаем None или другое значение по умолчанию

def filter_last_month_data(data):
    """Функция для фильтрации данных за последний месяц."""
    if "Time Series (Daily)" not in data:
        logger.error("Нет данных для символа: %s", data)
        return {}

    time_series = data["Time Series (Daily)"]
    last_month_data = {}
    today = datetime.now()
    last_month_date = today - timedelta(days=30)

    for date_str, daily_data in time_series.items():
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date >= last_month_date:
            last_month_data[date_str] = daily_data

    return last_month_data
