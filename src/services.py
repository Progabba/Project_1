import os
from typing import Any, Dict, List

import pandas as pd

from src.utils import load_excel_to_dataframe

current_dir = os.getcwd()
parrent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parrent_dir, "data")
file_path = os.path.join(data_dir, "operations.xls")


def search_phone_numbers(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """Поиск транзакций с мобильными номерами в описании."""
    phone_numbers = data[data["Описание"].str.contains(r"\+\d{1,2}\s\d{3}\s\d{2,3}-\d{2}-\d{2}", regex=True)].to_json(
        orient="records", force_ascii=False, indent=4
    )
    return phone_numbers


if __name__ == "__main__":
    data = load_excel_to_dataframe(file_path)
    print(search_phone_numbers(data))
