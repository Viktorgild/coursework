import pytest
from unittest.mock import patch, mock_open


@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get

@pytest.fixture
def mock_open_file():
    mock_data = '{"user_currencies": ["USD", "EUR"]}'
    with patch("builtins.open", new_callable=mock_open, read_data=mock_data):
        yield


@pytest.fixture
def mock_get_transactions():
    with patch("utils.get_transactions") as mock:
        yield mock

@pytest.fixture
def mock_get_exchange_rates():
    with patch("utils.get_exchange_rates") as mock:
        yield mock

@pytest.fixture
def mock_read_json_file():
    with patch("main.read_json_file") as mock:
        yield mock

@pytest.fixture
def mock_print(capsys):
    """Фикстура для перехвата вывода print."""
    yield capsys