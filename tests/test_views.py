import pytest

from src.views import top_transactions, greetings, calculate_card_details


def test_greetings(monkeypatch):
    # Тестируем разные времена суток
    test_cases = [
        (6, "Доброе утро"),
        (12, "Доброе утро"),
        (13, "Добрый день"),
        (17, "Добрый день"),
        (18, "Добрый вечер"),
        (23, "Добрый вечер"),
        (0, "Доброй ночи"),
        (5, "Доброй ночи"),
    ]

    for hour, expected in test_cases:
        monkeypatch.setattr("datetime.datetime.now", lambda: datetime.datetime(2023, 1, 1, hour))
        assert greetings() == expected


def test_calculate_card_details():
    transactions = [
        {"card_number": "1234567890123456", "amount": 100, "date": "2023-10-01", "time": "12:00"},
        {"card_number": "1234567890123456", "amount": 200, "date": "2023-10-02", "time": "13:00"},
        {"card_number": "9876543210987654", "amount": 150, "date": "2023-10-01", "time": "14:00"},
    ]

    result = calculate_card_details(transactions)

    assert "3456" in result
    assert result["3456"]["total_amount"] == 300
    assert result["3456"]["cashback"] == 3
    assert len(result["3456"]["transactions"]) == 2
    assert "7654" in result
    assert result["7654"]["total_amount"] == 150
    assert result["7654"]["cashback"] == 1
    assert len(result["7654"]["transactions"]) == 1


def test_top_transactions(mock_print):
    card_details = {
        "3456": {
            "last_four_digits": "3456",
            "total_amount": 300,
            "cashback": 3,
            "transactions": [
                {"date": "2023-10-01", "time": "12:00", "amount": 100},
                {"date": "2023-10-02", "time": "13:00", "amount": 200},
            ]
        }
    }

    top_transactions(card_details)

    captured = mock_print.readouterr()
    assert "Топ-5 транзакций для карты 3456:" in captured.out
    assert "1: Дата: 2023-10-02, Время: 13:00, Сумма: 200 рублей" in captured.out
    assert "2: Дата: 2023-10-01, Время: 12:00, Сумма: 100 рублей" in captured.out

