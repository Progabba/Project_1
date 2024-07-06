
import pytest
import pandas as pd

from src.reports import spending_by_category


# Фикстура для создания mock DataFrame
@pytest.fixture
def mock_df():
    data = {
        "Дата операции": ["01.01.2021 12:00:00", "15.02.2021 14:30:00", "10.03.2021 16:45:00", "20.03.2021 18:00:00"],
        "Категория": ["Фастфуд", "Фастфуд", "Транспорт", "Фастфуд"],
        "Сумма операции": [100, 150, 200, 250],
    }
    return pd.DataFrame(data)


# Тест для функции spending_by_category
def test_spending_by_category(mock_df):
    result = spending_by_category(mock_df, "Фастфуд", "2021-03-21 00:00:00")
    expected_sum = 500  # Сумма всех значений категории "Фастфуд"
    assert result == expected_sum


if __name__ == "__main__":
    pytest.main([__file__])
