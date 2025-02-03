import pytest
from freezegun import freeze_time

from src.utils import get_exchange_rates, get_transactions, read_json_file, filter_last_month_data
from unittest.mock import patch


def test_read_json_file(mock_open_file):
    data = read_json_file("dummy_path.json")
    assert data == {"user_currencies": ["USD", "EUR"]}


def test_get_transactions(mock_requests_get):
    mock_response = {"result": "success"}
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    with patch("os.getenv", return_value="dummy_api_key"):
        data = {"user_currencies": ["USD", "EUR"]}
        result = get_transactions(data)

        assert "EUR" in result
        assert result["EUR"] == mock_response
        mock_requests_get.assert_called_once()


@freeze_time("2023-10-02")  # Замораживаем время на 2 октября 2023 года
def test_get_exchange_rates(mock_requests_get):
    mock_response = {
        "Time Series (Daily)": {
            "2023-10-01": {"1. open": "100", "2. high": "110", "3. low": "90", "4. close": "105"},
            "2023-09-01": {"1. open": "90", "2. high": "100", "3. low": "80", "4. close": "85"},
            "2023-08-01": {"1. open": "80", "2. high": "90", "3. low": "70", "4. close": "75"},
        }
    }

    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    with patch("os.getenv", return_value="dummy_api_key"):
        user_data = {"user_stocks": ["AAPL"]}
        result = get_exchange_rates(user_data)

        assert "AAPL" in result
        assert "2023-10-01" in result["AAPL"]
        assert "2023-09-01" in result["AAPL"]  # Данные за сентябрь должны быть включены
        assert "2023-08-01" not in result["AAPL"]  # Данные за август не должны быть включены


def test_filter_last_month_data():
    # Дата для тестирования
    data = {
        "Time Series (Daily)": {
            "2023-10-01": {"1. open": "100", "2. high": "110", "3. low": "90", "4. close": "105"},
            "2023-09-01": {"1. open": "90", "2. high": "100", "3. low": "80", "4. close": "85"},
            "2023-08-01": {"1. open": "80", "2. high": "90", "3. low": "70", "4. close": "75"},
        }
    }

    # Вызов функции фильтрации
    filtered_data = filter_last_month_data(data)

    # Проверка, что данные за последний месяц присутствуют
    assert "2023-10-01" in filtered_data
    assert "2023-09-01" in filtered_data
    assert "2023-08-01" not in filtered_data  # Данные за август не должны быть включены