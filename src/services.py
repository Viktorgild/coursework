import json
import datetime
import logging

logging.basicConfig(level=logging.DEBUG, filename='../logs/services.log', format='%(asctime)s - %(name)s'
                                        ' - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# def read_json_file(filename):
#     with open(filename, 'r') as file:
#         data = json.load(file)
#     return data


def analyze_cashback(data, year, month):
    """Сервис позволяет проанализировать, какие категории были наиболее выгодными для выбора
    в качестве категорий повышенного кешбэка."""
    # Преобразование входных данных
    transactions = data['transactions']
    categories = data['categories']

    # Расчёт выгоды для каждой категории
    results = {}
    for category in categories:
        total_cashback = 0
        for transaction in transactions:
            if transaction['category'] == category and transaction['date'].year == year and transaction['date'].month == month:
                total_cashback += transaction['cashback']
        results[category] = total_cashback

    logging.info("Анализ кэшбэка за %s год, %s месяц успешно завершён", year, month)
    return results

# data = read_json_file('путь_к_вашему_файлу.json')

# Настройка логирования


# Пример использования функции
data = {
    'transactions': [
        {
            'category': 'Категория 1',
            'cashback': 500,
            'date': datetime.datetime(2023, 1, 1)
        },
        {
            'category': 'Категория 2',
            'cashback': 1000,
            'date': datetime.datetime(2023, 2, 1)
        }
    ],
    'categories': ['Категория 1', 'Категория 2']
}

result = analyze_cashback(data, 2023, 2)
print("{")
for key, value in result.items():
    print("\t\"{}\": {},".format(key, value))
print("}")