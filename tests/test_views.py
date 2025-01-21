from src.utils import get_exchange_rates
from src.views import top_transactions, get_transactions


def test_get_transactions(mocker):
    # Создание тестовых данных
    test_data = {
        "transactions": [
            {
                "card_number": "4242 4242 4242 4242",
                "amount": 1000,
                "date": "2023-01-01",
                "time": "12:00:00"
            },
            ...
        ]
    }

    # Мокинг функции read_json_file
    mocked_read_json_file = mocker.patch("read_json_file")
    mocked_read_json_file.return_value = test_data

    # Вызов функции get_transactions
    result = get_transactions()

    # Проверка результата
    assert result == test_data

def test_get_exchange_rates(mocker):
    # Создание тестовых данных
    test_data = [
        {"S&P500": 3000},
        ...
    ]

    # Мокинг функции get_exchange_rates
    mocked_get_exchange_rates = mocker.patch("get_exchange_rates")
    mocked_get_exchange_rates.return_value = test_data

    # Вызов функции get_exchange_rates
    result = get_exchange_rates("S&P500")

    # Проверка результата
    assert result == test_data["S&P500"]

def test_top_transactions(mocker):
    # Создание тестовых данных
    test_data = {
        "transactions": [
            {
                "card_number": "4242 4242 4242 4242",
                "amount": 1000,
                "date": "2023-01-01",
                "time": "12:00:00"
            },
            ...
        ]
    }

    # Мокинг функций get_transactions и get_exchange_rates
    mocked_get_transactions = mocker.patch("get_transactions")
    mocked_get_transactions.return_value = test_data
    mocked_get_exchange_rates = mocker.patch("get_exchange_rates")

    # Вызов функции top_transactions
    result = top_transactions()

    # Проверка результатов
    for i, transaction in enumerate(result):
        assert i + 1 == transaction["id"]
        assert transaction["amount"] == 1000
        assert transaction["date"] == "2"


