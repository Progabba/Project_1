import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.utils import load_excel_to_dataframe

current_dir = os.getcwd()
parrent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parrent_dir, "data")
file_path = os.path.join(data_dir, "operations.xls")
json_path = os.path.join(parrent_dir, "user_settings.json")
log_dir = os.path.join(parrent_dir, "logs")
log_path = os.path.join(log_dir, "eports.log")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=log_path,  # Запись логов в файл
    filemode="w",
)  # Перезапись файла при каждом запуске


df = load_excel_to_dataframe(file_path)

logging.info(f"Дата фрейм наш {df}")


def write_report_default(func):
    """Декоратор без параметра, записывающий отчет в файл с именем по умолчанию."""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        file_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(f"../reports/{file_name}", "w", encoding="utf-8") as file:
            file.write(f"Отчет создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Результат: {result}\n")
        return result

    return wrapper


def write_report(file_name):
    """Декоратор с параметром, принимающий имя файла."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(f"../reports/{file_name}", "w", encoding="utf-8") as file:
                file.write(f"Отчет создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Результат: {result}\n")
            return result

        return wrapper

    return decorator


@write_report_default
@write_report("custom_report.txt")
def spending_by_category(df: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    if date is None:
        date = datetime.now()
        logging.info(f"Дата {date}")
    else:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")  # Преобразование строки в объект datetime
    logging.info(f"Дата {date}")
    start_date = date - timedelta(days=90)
    logging.info(f"Старт дейт {start_date}")

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")  # Преобразование в datetime
    logging.info(f"Дата операции {df['Дата операции']}")

    filtered_df = df[
        (df["Дата операции"] >= start_date) & (df["Дата операции"] <= date) & (df["Категория"] == category)
    ]
    summ_ = filtered_df["Сумма операции"].sum()
    positive_value = abs(summ_)
    return positive_value


if __name__ == "__main__":
    print(spending_by_category(df, "Фастфуд", "2021-07-06 19:27:30"))
