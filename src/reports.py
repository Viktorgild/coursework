import datetime
import json
import logging

import pandas as pd

logging.basicConfig(level=logging.DEBUG, filename='../logs/reports.log', format='%(asctime)s - %(name)s'
                                        ' - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

df = pd.read_excel("../data/operations.xlsx")
df.set_index('Категория', drop=False, inplace=True)
df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True).dt.date

def report_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        filename = kwargs.get("filename", "report_{}.json".format(func.__name__))
        try:
            with open(filename, "w") as file:
                json.dump(result, file)
        except Exception as e:
            print("Ошибка при записи файла:", e)
        return result

    return wrapper


def generate_report(transactions, category, date=None):
    """
    Функция для генерации отчёта по категории транзакций за определённый период времени.
    """

    if date is None:
        date = datetime.date.today()
    three_months_ago = date - datetime.timedelta(days=90)  # 3 месяца в днях

    filtered_transactions = transactions.loc[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= date)
    ]

    total_spent = filtered_transactions["Сумма операции"].sum()

    result = {
        "Категория": category,
        "Дата операции": str(date),
        "Всего потрачено": total_spent.astype(str)
    }
    logging.info("Отчет по категории %s за %s успешно сгенерирован", category, str(date))
    return result

@report_decorator
def generate_category_report(category):
    json_data = generate_report(df, category)

    with open('../data/output_file.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)

generate_category_report('Продукты')
