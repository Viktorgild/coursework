import datetime
import pprint

from utils import get_exchange_rates, get_transactions, read_json_file


def greetings() -> str:
    """Функция, которая возвращает строку с приветствием в зависимости от времени."""
    hour = int(datetime.datetime.now().strftime("%H"))
    if 6 <= hour <= 12:
        return "Доброе утро"
    elif 13 <= hour <= 17:
        return "Добрый день"
    elif 18 <= hour <= 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


print(greetings())


def calculate_card_details(transactions):
    """
    Функция для расчёта последних 4 цифр номера карты, общей суммы расходов и кешбэка для каждой карты.
    :param transactions: список транзакций
    :return: словарь с деталями по каждой карте
    """

    # Словарь для хранения деталей по каждой карте
    card_details = {}

    for transaction in transactions:
        # Получение номера карты из транзакции
        try:
            card_number = transaction["card_number"]
        except KeyError as e:
            print("Ошибка: ключ 'card_number' не найден в словаре транзакций.")
            continue

        # Извлечение последних 4 цифр номера карты
        try:
            last_four_digits = card_number[-4:]
        except Exception as e:
            print("Ошибка при извлечении последних 4 цифр номера карты:", e)
            continue

        total_amount = sum(
            [transaction["amount"] for transaction in transactions if transaction["card_number"] == card_number]
        )
        cashback = total_amount // 100

        card_details[last_four_digits] = {
            "last_four_digits": last_four_digits,
            "total_amount": total_amount,
            "cashback": cashback,
        }

    return card_details


def top_transactions(card_details):
    """
    Выводит топ-5 транзакций по сумме для всех карт.
    :param card_details: словарь с информацией о транзакциях
    """

    # Создаём список для хранения топ-5 транзакций
    top_transactions = []

    # Проходимся по каждой карте
    for _, details in card_details.items():
        # Сортируем транзакции по убыванию суммы
        sorted_transactions = sorted(details["transactions"], key=lambda x: x["amount"], reverse=True)

        # Добавляем топ-5 транзакций в общий список
        top_transactions.extend(sorted_transactions[:5])

    print("Топ-5 транзакций:")
    # Выводим топ-5 транзакций, пронумеровав их
    try:
        for i, transaction in enumerate(top_transactions):
            print(
                f"{i + 1}: Дата: {transaction['date']}, Время: {transaction['time']}, Сумма: {transaction['amount']} рублей"
            )
    except Exception as e:
        print("Произошла ошибка:", e)
    return top_transactions


rates = get_transactions(read_json_file("../user_settings.json"))

# Использование полученных данных
pprint.pprint(rates)

result_dict = get_exchange_rates("S&P500")
pprint.pprint(result_dict)
