import datetime
import json
import logging
from .logging_config import setup_logger

# Настраиваем логирование
logger = setup_logger("services_loger", "../logs/services.log")


def read_json_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def analyze_cashback(data, year, month):
    """Сервис позволяет проанализировать, какие категории были наиболее выгодными для выбора
    в качестве категорий повышенного кешбэка."""
    # Преобразование входных данных
    transactions = data["transactions"]
    categories = data["categories"]

    # Расчёт выгоды для каждой категории
    results = {}
    for category in categories:
        total_cashback = 0
        for transaction in transactions:
            if (
                transaction["category"] == category
                and transaction["date"].year == year
                and transaction["date"].month == month
            ):
                total_cashback += transaction["cashback"]
        results[category] = total_cashback

    logging.info("Анализ кэшбэка за %s год, %s месяц успешно завершён", year, month)
    return results


