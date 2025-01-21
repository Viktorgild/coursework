import json
import logging
import os
from venv import logger

import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG, filename='../logs/utils.log', format='%(asctime)s - %(name)s'
                                        ' - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


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
    """Функция для получения последнего курса акций."""
    api = os.getenv("api_key")
    logger.debug("Начало запроса")
    try:
        if isinstance(symbol_or_data, dict):
            # Если передан словарь
            result_dict = {}
            for symbol in symbol_or_data["user_stocks"]:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api}"
                r = requests.get(url)
                result_dict[symbol] = r.json()
        else:
            # Если передан один символ
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol_or_data}&apikey={api}"
            r = requests.get(url)
            result_dict = {symbol_or_data: r.json()}

            return result_dict
    except Exception as e:
        logger.error("Произошла ошибка:", e)
        print("Произошла ошибка:", e)


load_dotenv()
