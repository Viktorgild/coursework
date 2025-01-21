from src.services import analyze_cashback
import pytest
from unittest.mock import patch

def test_analyze_cashback():
    # Подготовка тестовых данных
    data = {
        "transactions": [
            {
                "category": "Одежда",
                "date": "2023-01-01",
                "cashback": 10
            },
            {
                "category": "Еда",
                "date": "2023-02-01",
                "cashback": 5
            }
        ],
        "categories": ["Одежда", "Еда"]
    }

    # Тестирование функции
    result = analyze_cashback(data, 2023, 1)

    assert result == {
        "Одежда": 10,
        "Еда": 0
    }, "Результаты должны соответствовать ожидаемым значениям."

@patch("logging.info")
def test_logging(mock_info):
    # Проверка логирования
    analyze_cashback({}, 2023, 1)
    mock_info.assert_called_once_with("Анализ кэшбэка за 2023 год, 1 месяц успешно завершён")

# Дополнительные тесты для проверки различных сценариев

def test_empty_data():
    with pytest.raises(KeyError):
        analyze_cashback({}, 2023, 1)  # Проверить обработку пустых или некорректных данных

def test_invalid_year_month():
    with pytest.raises(ValueError):
        analyze_cashback({"transactions": []}, 2022, 3) # Проверить обработку некорректного года или месяца

def test_missing_category():
    data = {"transactions": [{"category": "Одежда", "date": "2023-01-01", "cashback": 10}], "categories": ["Еда"]}
    with pytest.raises(KeyError):
        analyze_cashback(data, 2023, 1), "Проверить обработку отсутствующей категории в данных"
