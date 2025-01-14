import json
from datetime import datetime

def analyze_cashback(data, year, month):
    # 1. Преобразуем данные в удобный формат
    categories = {}
    for transaction in data:
        category = transaction['category']
        if category not in categories:
            categories[category] = 0
        categories[category] += transaction['amount']

    # 2. Рассчитаем сумму кешбэка для каждой категории
    result = {}
    now = datetime.strptime(f"{year}-{month}-01", "%Y-%m-01")
    while now <= datetime.strptime(f"{year}-{month}-31", "%Y-%m-31"):
        month_data = {
            'date': now.strftime("%Y-%m-%d"),
            'transactions': []
        }
        for category, amount in categories.items():
            if now.day in range(1, 32):  # Проверяем, есть ли транзакции за этот день
                month_data['transactions'].append({
                    'category': category,
                    'amount': amount
                })
        result[now.strftime("%b")] = month_data
        now += datetime.timedelta(days=1)

    return result

# Пример использования функции
data = [
    {
        'category': 'Категория 1',
        'amount': 1000
    },
    {
        'category': 'Категория 2',
        'amount': 2000
    },
    {
        'category': 'Категория 3',
        'amount': 500
    }
]

result = analyze_cashback(data, 2023, 12)
json_result = json.dumps(result, ensure_ascii=False)
print(json_result)
