import json

import pandas as pd
import pytest

from src.services import search_phone_numbers


# Пример теста
def test_search_phone_numbers():
    data = {
        "Описание": ["Call +7 123 456-78-90", "Email me", "Call +7 789 123-45-67", "No phone number"],
        "Сумма операции": [100, 200, 300, 400],
    }
    df = pd.DataFrame(data)

    expected_result = [
        {"Описание": "Call +7 123 456-78-90", "Сумма операции": 100},
        {"Описание": "Call +7 789 123-45-67", "Сумма операции": 300},
    ]

    # Вызов функции
    result = search_phone_numbers(df)

    # Проверка результата
    assert json.loads(result) == expected_result


if __name__ == "__main__":
    pytest.main([__file__])
