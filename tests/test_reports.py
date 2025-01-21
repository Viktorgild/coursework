import logging

from src.reports import generate_report

import pytest
from unittest.mock import patch

def test_generate_report(mocker):
    # Подготовка тестовых данных
    transactions = {
        "Дата операции": ["2023-01-01", "2023-02-01"],
        "Сумма операции": [10, 5],
        "Категория": ["Одежда", "Еда"]
    }
    category = "Одежда"
    date = "2023-03-01"

    expected_result = {
        "Категория": category,
        "Дата операции": date,
        "Всего потрачено": "10"
    }

    # Тестирование функции
    with patch("builtins.open", mocker.mock_open()) as mock_file:
        result = generate_report(transactions, category, date)

    assert result == expected_result

    mock_file.assert_called_once_with("../data/report.json", "w", encoding="utf-8")
    logging.info.assert_called_once()

@patch("logging.debug")
@patch("requests.get")
def test_logging(mock_requests, mock_debug):
    # Проверка логирования
    generate_report({}, "Одежда")
    mock_debug.assert_called_once_with("Начало запроса")
    mock_requests.assert_called_once()

# Дополнительные тесты для проверки различных сценариев

def test_empty_data():
    with pytest.raises(KeyError):
        generate_report({}, None), "Проверить обработку пустых или некорректных данных"

def test_invalid_date():
    with pytest.raises(ValueError):
        generate_report({"Дата операции": []}, "Одежда"), "Проверить обработку некорректной даты"

def test_missing_category():
    data = {"Дата операции": ["2023-01-01", "2023-02-01"], "Сумма операции": [10, 5]}
    with pytest.raises(KeyError):
        generate_report(data, None), "Проверить обработку отсутствующей категории в данных"

def test_response_code_200():
    response = {
        'status_code': 200,
        'text': '{"rate": 1.23}'
    }
    mock_response = patch('requests.get', return_value=response)
    with mock_response as m:
        result_dict = generate_report({'Дата операции': ['2023-01-01']}, 'Одежда')
        assert result_dict['Одежда'] == '{"rate": 1.23}', "Проверка корректности обработки ответа с кодом 200"

def test_response_code_404():
    response = {
        'status_code': 404,
        'text': 'Ошибка запроса'
    }
    mock_response = patch('requests.get', return_value=response)
    with mock_response as m:
        result_dict = generate_report({'Дата операции': ['2023-01-01']}, 'Еда')
        assert result_dict['Еда'] is None, "Проверка обработки ответа с кодом ошибки 404"