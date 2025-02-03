import json
import logging
import os
from datetime import datetime, timedelta
from venv import logger

import requests
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG,
    filename="../logs/utils.log",
    encoding="utf-8",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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

        payload = {}
        headers = {"apikey": os.getenv("API_KEY")}

        logger.debug("Начало запроса")

        try:
            response = requests.get(url, headers=headers, data=payload)

            status_code = response.status_code
            result = response.text

            if response.status_code == 200:
                logger.info("Успешный запрос")
            else:
                logger.error("Ошибка запроса: {}".format(response.text))

            result_dict[symbol] = result
        except Exception as e:
            logger.exception("Произошла ошибка: {}".format(e))

    return result_dict


load_dotenv()


def get_exchange_rates(symbol_or_data):
    """Функция для получения курсов акций за последний месяц."""
    api = os.getenv("api_key")
    logger.debug("Начало запроса")
    try:
        if isinstance(symbol_or_data, dict):
            # Если передан словарь
            result_dict = {}
            for symbol in symbol_or_data["user_stocks"]:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api}"
                r = requests.get(url)
                data = r.json()
                # Фильтруем данные за последний месяц
                result_dict[symbol] = filter_last_month_data(data)
            return result_dict  # Возвращаем результат
        else:
            # Если передан один символ
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol_or_data}&apikey={api}"
            r = requests.get(url)
            data = r.json()
            result_dict = {symbol_or_data: filter_last_month_data(data)}
            return result_dict
    except Exception as e:
        logger.error("Произошла ошибка: %s", e)
        print("Произошла ошибка:", e)


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
        date = datetime.strptime(date_str, '%Y-%m-%d')
        if date >= last_month_date:
            last_month_data[date_str] = daily_data

    return last_month_data
