
import logging
import os

import pandas as pd
from pandas import DataFrame

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/utils.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

current_dir = os.getcwd()
parrent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parrent_dir, 'data')
file_path = os.path.join(data_dir, 'operations.xls')


def load_excel_to_dataframe(file_path: str) -> DataFrame:
    """Функция читает эксель файл и возвращает дата фрейм"""
    df = pd.read_excel(file_path)
    logger.info(f"Успешно загружены {len(df)} операций")
    return df


if __name__ == '__main__':
    print(file_path)
    df = load_excel_to_dataframe(file_path)
    print(df)


