import pytest
from src.utils import get_exchange_rates, get_transactions
from unittest.mock import patch

def test_get_transactions():
    # Подготовка тестовых данных
    data = {
        "user_currencies": ["USD", "EUR", "GBP"]
    }

    # Тестирование функции
    result_dict = get_transactions(data)

    assert result_dict == {
        "USD": None,
        "EUR": None,
        "GBP": None
    }, "Результаты должны соответствовать ожидаемым значениям."

@patch("logging.debug")
@patch("requests.get")
def test_logging(mock_requests, mock_debug):
    # Проверка логирования
    get_transactions({})
    mock_debug.assert_called_once_with("Начало запроса")
    mock_requests.assert_called_once()

# Дополнительные тесты для проверки различных сценариев

def test_empty_data():
    with pytest.raises(KeyError):
        get_transactions({}, "error")  # Проверить обработку пустых или некорректных данных

def test_invalid_url():
    with pytest.raises(ValueError):
        get_transactions({"user_currencies": []}) # Проверить обработку некорректного URL

def test_missing_symbol():
    data = {"user_currencies": ["EUR", "GBP"]}
    with pytest.raises(KeyError):
        get_transactions(data), "Проверить обработку отсутствующего символа в данных"

def test_response_code_200():
    response = {
        'status_code': 200,
        'text': '{"rate": 1.23}'
    }
    mock_response = patch('requests.get', return_value=response)
    with mock_response as m:
        result_dict = get_transactions({'user_currencies': ['USD', 'EUR']})
        assert result_dict['EUR'] == '{"rate": 1.23}', "Проверка корректности обработки ответа с кодом 200"

def test_response_code_404():
    response = {
        'status_code': 404,
        'text': 'Ошибка запроса'
    }
    mock_response = patch('requests.get', return_value=response)
    with mock_response as m:
        result_dict = get_transactions({'user_currencies': ['USD']})
        assert result_dict['USD'] is None, "Проверка обработки ответа с кодом ошибки 404"


def test_get_exchange_rates():
    # Подготовка тестовых данных
    data = {
        "user_stocks": ["AAPL", "MSFT"]
    }

    # Тестирование функции
    result_dict = get_exchange_rates(data)

    assert result_dict == {
        "AAPL": None,
        "MSFT": None
    }, "Результаты должны соответствовать ожидаемым значениям."

@patch("logging.debug")
@patch("requests.get")
def test_logging(mock_requests, mock_debug):
    # Проверка логирования
    get_exchange_rates({})
    mock_debug.assert_called_once_with("Начало запроса")
    mock_requests.assert_called_once()

# Дополнительные тесты для проверки различных сценариев

def test_emptyy_data():
    with pytest.raises(KeyError):
        get_exchange_rates({}, "error")  # Проверить обработку пустых или некорректных данных

def test_invalidd_url():
    with pytest.raises(ValueError):
        get_exchange_rates({"user_stocks": []}) # Проверить обработку некорректного URL

def test_missingg_symbol():
    data = {"user_stocks": ["MSFT"]}
    with pytest.raises(KeyError):
        get_exchange_rates(data), "Проверить обработку отсутствующего символа в данных"

def test_responsee_code_200():
    response = {
        'status_code': 200,
        'text': '{"rate": 1.23}'
    }
    mock_response = patch('requests.get', return_value=response)
    with mock_response as m:
        result_dict = get_exchange_rates({'user_stocks': ['AAPL']})
        assert result_dict['AAPL'] == '{"rate": 1.23}', "Проверка корректности обработки ответа с кодом 200"

def test_responsee_code_404():
    response = {
        'status_code': 404,
        'text': 'Ошибка запроса'
    }
    mock_response = patch('requests.get', return_value=response)
    with mock_response as m:
        result_dict = get_exchange_rates({'user_stocks': ['MSFT']})
        assert result_dict['MSFT'] is None, "Проверка обработки ответа с кодом ошибки 404"