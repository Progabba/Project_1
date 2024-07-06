from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import load_excel_to_dataframe


def test_load_excel_to_dataframe():
    # Создаем тестовый датафрейм
    test_data = {"Колонка1": [1, 2, 3], "Колонка2": ["a", "b", "c"]}
    test_df = pd.DataFrame(test_data)

    # Используем patch для имитации pd.read_excel
    with patch("pandas.read_excel", return_value=test_df) as mock_read_excel:
        # Вызываем тестируемую функцию
        result = load_excel_to_dataframe("fake_path.xlsx")

        # Проверяем, что функция pd.read_excel была вызвана с правильным аргументом
        mock_read_excel.assert_called_once_with("fake_path.xlsx")

        # Проверяем, что результат функции совпадает с ожидаемым датафреймом
        pd.testing.assert_frame_equal(result, test_df)


if __name__ == "__main__":
    pytest.main([__file__])
