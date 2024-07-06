import json
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from src.views import (
    main_views_foo,
    get_stock_prices,
    get_currency_rates,
    get_top_transactions,
    get_card_summary,
    get_greeting,
)


def test_get_greeting():
    assert get_greeting("2024-04-06 06:00:00") == "Доброе утро"
    assert get_greeting("2024-04-06 13:00:00") == "Добрый день"
    assert get_greeting("2024-04-06 19:00:00") == "Добрый вечер"
    assert get_greeting("2024-04-06 23:00:00") == "Доброй ночи"


def test_get_card_summary():
    data = {
        "Номер карты": ["1234567890123456", "1234567890123456", "9876543210987654"],
        "Сумма платежа": [100, 200, 300],
    }
    df = pd.DataFrame(data)
    result = get_card_summary(df)
    expected = [
        {"last_digits": "3456", "total_spent": 300.0, "cashback": 3.0},
        {"last_digits": "7654", "total_spent": 300.0, "cashback": 3.0},
    ]
    assert result == expected


def test_get_top_transactions():
    data = {
        "Дата операции": ["01.01.2024", "15.02.2024", "10.03.2024", "20.03.2024"],
        "Сумма платежа": [100, 200, 300, 150],
        "Категория": ["Еда", "Транспорт", "Одежда", "Еда"],
        "Описание": ["Покупка еды", "Проезд", "Покупка одежды", "Покупка еды"],
    }
    df = pd.DataFrame(data)
    result = get_top_transactions(df, top_n=2)
    expected = [
        {"date": "10.03.2024", "amount": 300, "category": "Одежда", "description": "Покупка одежды"},
        {"date": "15.02.2024", "amount": 200, "category": "Транспорт", "description": "Проезд"},
    ]
    assert result == expected


def test_get_currency_rates():
    mock_user_settings = {"user_currencies": ["USD", "EUR"]}
    mock_response = {"rates": {"USD": 0.013, "EUR": 0.011}}

    with patch("builtins.open", MagicMock()) as mock_open, patch(
        "json.load", MagicMock(return_value=mock_user_settings)
    ), patch("requests.get", MagicMock(return_value=MagicMock(status_code=200, json=lambda: mock_response))):
        result = get_currency_rates()
        expected = [{"currency": "USD", "rate": 1 / 0.013}, {"currency": "EUR", "rate": 1 / 0.011}]
        assert result == expected


def test_get_stock_prices():
    mock_user_settings = {"user_stocks": ["AAPL", "GOOGL"]}
    mock_response = {"c": 150}

    with patch("builtins.open", MagicMock()) as mock_open, patch(
        "json.load", MagicMock(return_value=mock_user_settings)
    ), patch("requests.get", MagicMock(return_value=MagicMock(status_code=200, json=lambda: mock_response))):
        result = get_stock_prices("dummy_api_key")
        expected = [{"stock": "AAPL", "price": 150}, {"stock": "GOOGL", "price": 150}]
        assert result == expected


def test_main_views_foo():
    data_time = "2024-04-06 19:40:15"
    data = {
        "Дата операции": ["01.01.2024", "15.02.2024", "10.03.2024", "20.03.2024"],
        "Сумма платежа": [100, 200, 300, 150],
        "Категория": ["Еда", "Транспорт", "Одежда", "Еда"],
        "Описание": ["Покупка еды", "Проезд", "Покупка одежды", "Покупка еды"],
        "Номер карты": ["1234567890123456", "1234567890123456", "9876543210987654", "1234567890123456"],
    }
    df = pd.DataFrame(data)

    with patch("src.views.load_excel_to_dataframe", MagicMock(return_value=df)), patch(
        "src.views.get_currency_rates", MagicMock(return_value=[{"currency": "USD", "rate": 75}])
    ), patch("src.views.get_stock_prices", MagicMock(return_value=[{"stock": "AAPL", "price": 150}])):
        result = main_views_foo(data_time)
        result_dict = json.loads(result)

        assert result_dict["greeting"] == "Добрый вечер"
        assert result_dict["currency_rates"] == [{"currency": "USD", "rate": 75}]
        assert result_dict["stock_prices"] == [{"stock": "AAPL", "price": 150}]


if __name__ == "__main__":
    pytest.main([__file__])
