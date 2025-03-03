import datetime
import os
import json
from typing import Optional
import pandas as pd
from .logging_config import setup_logger

# Настройка логгера
logger = setup_logger("reports_logger", "../logs/reports.log")

def read_operations(file_path: str) -> pd.DataFrame:
    """Функция для чтения операций из Excel файла."""
    try:
        logger.info(f"Попытка чтения файла: {file_path}")
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден: {file_path}")
            return pd.DataFrame()

        df = pd.read_excel(file_path)
        logger.info("Файл успешно прочитан")
        logger.info(f"Содержимое файла:\n{df}")  # Логируем содержимое файла

        # Проверяем наличие необходимых колонок
        required_columns = ["Категория", "Дата операции", "Сумма операции"]
        if not all(col in df.columns for col in required_columns):
            logger.error(f"Файл не содержит необходимых колонок: {required_columns}")
            return pd.DataFrame()

        # Преобразуем дату
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%Y-%m-%d", errors="coerce")
        if df["Дата операции"].isnull().any():
            logger.error("Некорректный формат даты в колонке 'Дата операции'")
            return pd.DataFrame()

        df.set_index("Категория", drop=False, inplace=True)
        logger.info("Операции успешно прочитаны")
        return df
    except Exception as e:
        logger.error(f"Ошибка при чтении операций из файла: {e}")
        return pd.DataFrame()


def log(filename: str):
    def report_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
                return result
            except Exception as e:
                logger.error("Ошибка при выполнении функции %s: %s", func.__name__, e)
                return {}
        return wrapper
    return report_decorator

@log("../data/report.json")
def generate_report(transactions: pd.DataFrame, category: str, date: Optional[str] = None):
    """
    Функция для генерации отчёта по категории транзакций за определённый период времени.
    """
    if transactions.empty:
        logger.warning("Передан пустой DataFrame")
        return {}

    if date is None:
        todate = datetime.datetime.now().date()
    else:
        try:
            todate = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            logger.error("Некорректный формат даты: %s", date)
            return {}

    # Вычисляем дату начала периода (3 месяца назад)
    three_months_ago = todate - datetime.timedelta(days=90)

    # Фильтрация данных
    filtered_transactions = transactions.loc[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"].dt.date >= three_months_ago)
        & (transactions["Дата операции"].dt.date <= todate)  # Используем <= вместо <
    ]

    if filtered_transactions.empty:
        logger.warning("Нет данных для категории %s за указанный период", category)
        return {}

    # Преобразуем total_spent в стандартный int
    total_spent = int(filtered_transactions["Сумма операции"].sum())
    result = {"Категория": category, "Дата операции": str(todate), "Всего потрачено": total_spent}

    logger.info("Отчет по категории %s за %s успешно сгенерирован", category, str(todate))
    return result

# Пример использования
if __name__ == "__main__":
    operations_file_path = "./data/operations.xlsx"
    df = read_operations(operations_file_path)

    if not df.empty:
        data = "2021-12-31"
        category = "Супермаркеты"
        generate_report(df, category, data)