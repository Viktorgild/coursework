import json
from pandas import DataFrame
from datetime import date

def report_decorator(func):
    """
    Декоратор для функций-отчетов, записывающий результат в файл.
    Если имя файла не указано, то используется название по умолчанию.
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        filename = kwargs.get("filename", "report_{}.json".format(func.__name__))
        with open(filename, "w") as file:
            json.dump(result, file)
        return result

    return wrapper

# Функция для формирования отчета
def generate_report(transactions_df, category, date=None):
    if date is None:
        date = date.today()
    three_months_ago = date - date.relativedelta(months=3)
    filtered_transactions = transactions_df[
        (transactions_df["category"] == category) &
        (transactions_df["date"] >= three_months_ago)
    ]
    total_spent = filtered_transactions["amount"].sum()

    result = {
        "category": category,
        "date": date,
        "total_spent": total_spent
    }
    return result

@report_decorator
def generate_category_report(transactions_df, category):
    return generate_report(transactions_df, category)

# Пример использования
if __name__ == "__main__":
    transactions_df = DataFrame({
        "category": ["food", "transport", "entertainment"],
        "amount": [100, 200, 50],
        "date": [date(2023, 1, 1), date(2023, 2, 15), date(2023, 3, 1)]
    })
    generate_category_report(transactions_df, "food")
    print("Отчет записан в файл 'report_generate_category_report.json'.")