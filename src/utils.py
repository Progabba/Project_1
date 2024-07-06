import logging
import os

import pandas as pd
from pandas import DataFrame

current_dir = os.getcwd()
parrent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parrent_dir, "data")
file_path = os.path.join(data_dir, "operations.xls")

log_dir = os.path.join(parrent_dir, "logs")
log_path = os.path.join(log_dir, "utils.log")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=log_path,  # Запись логов в файл
    filemode="w",
)  # Перезапись файла при каждом запуске


def load_excel_to_dataframe(file_path: str) -> DataFrame:
    """Функция читает эксель файл и возвращает дата фрейм"""
    df = pd.read_excel(file_path)
    logging.info(f"Успешно загружены {len(df)} операций")
    return df


if __name__ == "__main__":
    print(file_path)
    df = load_excel_to_dataframe(file_path)
    print(df)
