import datetime
import json
import logging
from typing import Optional

import pandas as pd

logging.basicConfig(
    level=logging.DEBUG,
    filename="../logs/reports.log",
    encoding="utf-8",
    format="%(asctime)s - %(name)s" " - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

df = pd.read_excel("../data/operations.xlsx")
df.set_index("Категория", drop=False, inplace=True)
df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)


def log(filename: str):
    def report_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            try:
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(
                        result, file, ensure_ascii=False, indent=4
                    )  # Добавлен параметр indent для улучшения читаемости JSON-структур
            except Exception as e:
                print("Ошибка при записи файла:", e)
            return result

        return wrapper

    return report_decorator


@log("../data/report.json")
def generate_report(transactions, category, date: Optional[str] = None):
    """
    Функция для генерации отчёта по категории транзакций за определённый период времени.
    """

    if date is None:
        todate = datetime.datetime.now().date()
    e_months_ago = todate - datetime.timedelta(days=90)  # 3 месяца в днях
    three_months_ago = e_months_ago.replace()
    print(type(transactions["Дата операции"].dt.date), type(data))
    filtered_transactions = transactions.loc[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"].dt.date >= three_months_ago)
        & (transactions["Дата операции"].dt.date < todate)
    ]
    date = todate

    total_spent = filtered_transactions["Сумма операции"].sum()
    result = {"Категория": category, "Дата операции": str(date), "Всего потрачено": total_spent.astype(str)}
    logging.info("Отчет по категории %s за %s успешно сгенерирован", category, str(date))
    return result


data = "2021-12-31"
date_obj = datetime.datetime.strptime(data, "%Y-%m-%d")
category = input("Введите категорию")
generate_report(df, category)
