import datetime
import json
from typing import Optional
import pandas as pd
from .logging_config import setup_logger

# Настройка логгера
logger = setup_logger("reports_logger", "../logs/reports.log")

def read_operations(file_path: str) -> pd.DataFrame:
    """Функция для чтения операций из Excel файла."""
    try:
        df = pd.read_excel(file_path)
        df.set_index("Категория", drop=False, inplace=True)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        logger.info("Операции успешно прочитаны из файла: %s", file_path)
        return df
    except Exception as e:
        logger.error("Ошибка при чтении операций из файла: %s", e)
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки

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
    if date is None:
        todate = datetime.datetime.now().date()
    else:
        todate = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    e_months_ago = todate - datetime.timedelta(days=90)  # 3 месяца в днях
    three_months_ago = e_months_ago  # Убираем .date(), так как это уже объект date

    filtered_transactions = transactions.loc[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"].dt.date >= three_months_ago)
        & (transactions["Дата операции"].dt.date < todate)
    ]

    total_spent = filtered_transactions["Сумма операции"].sum()
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
