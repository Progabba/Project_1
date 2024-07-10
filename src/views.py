import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

from src.utils import load_excel_to_dataframe

load_dotenv()


finnhub_key = os.getenv("FINNHUB")


current_dir = os.getcwd()
parrent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parrent_dir, "data")
file_path = os.path.join(data_dir, "operations.xls")
json_path = os.path.join(parrent_dir, "user_settings.json")
log_dir = os.path.join(parrent_dir, "logs")
log_path = os.path.join(log_dir, "views.log")

df = load_excel_to_dataframe(file_path)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=log_path,  # Запись логов в файл
    filemode="w",
)  # Перезапись файла при каждом запуске


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от текущего времени суток"""
    current_time = datetime.now()
    hour = current_time.hour
    if 5 <= hour < 12:
        logging.info("Доброе утро")
        return "Доброе утро"
    elif 12 <= hour < 18:
        logging.info("Добрый день")
        return "Добрый день"
    elif 18 <= hour < 23:
        logging.info("Добрый вечер")
        return "Добрый вечер"
    else:
        logging.info("Доброй ночи")
        return "Доброй ночи"


def get_card_summary(df: pd.DataFrame) -> list:
    """Возвращает информацию по каждой карте: последние 4 цифры, общая сумма расходов, кешбэк"""
    card_summary = []  # Создаем пустой список для хранения информации по картам
    for card in df["Номер карты"].unique():  # Перебираем уникальные значения из столбца 'Номер карты'
        logging.info(f"Обработка карты: {card}")
        card_df = df[df["Номер карты"] == card]  # Фильтруем датафрейм по текущей карте
        total_spent = card_df["Сумма платежа"].sum()  # Считаем общую сумму расходов для текущей карты
        logging.info(f"Сумма расходов{total_spent}")
        cashback = total_spent / 100  # Рассчитываем кешбэк как 1% от общей суммы расходов
        # Добавляем информацию по текущей карте в список card_summary
        card_summary.append(
            {
                "last_digits": str(card)[-4:],  # Последние 4 цифры номера карты
                "total_spent": abs(round(total_spent, 2)),  # Общая сумма расходов
                "cashback": abs(round(cashback, 2)),  # Кешбэк
            }
        )
    logging.info(f"Результат {card_summary}")
    return card_summary


def get_top_transactions(df: pd.DataFrame, top_n: int = 5) -> list:
    """Возвращает топ-N транзакций по сумме платежа"""
    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], dayfirst=True
    )  # Преобразуем столбец 'Дата операции' в datetime с dayfirst=True
    top_transactions = df.nlargest(top_n, "Сумма платежа")
    top_transactions = top_transactions[["Дата операции", "Сумма платежа", "Категория", "Описание"]]
    top_transactions["Дата операции"] = top_transactions["Дата операции"].dt.strftime("%d.%m.%Y")
    formatted_transactions = []
    for index, row in top_transactions.iterrows():
        formatted_transactions.append(
            {
                "date": row["Дата операции"],
                "amount": row["Сумма платежа"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
    logging.info(f"Результат {formatted_transactions}")
    return formatted_transactions


def get_currency_rates() -> list:
    # Загружаем user_settings.json
    with open(json_path) as file:
        user_settings = json.load(file)

    user_currencies = user_settings.get("user_currencies", [])
    logging.info(f"Валюта из юзер файла: {user_currencies}")
    url = "https://api.exchangerate-api.com/v4/latest/RUB"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        logging.info(f"Джайсон файл из апи: {data}")
        rates = []
        for currency in user_currencies:
            if currency in data.get("rates", {}):
                rate = 1 / data["rates"][currency]
                rates.append({"currency": currency, "rate": rate})

        return rates
    return []


def get_stock_prices(finnhub_key: str) -> list:
    """Возвращает стоимость акций для символов из user_settings.json"""

    # Загружаем user_settings.json
    with open(json_path) as file:
        user_settings = json.load(file)

    symbols = user_settings.get("user_stocks", [])
    logging.info(f"Символы для запроса: {symbols}")
    prices = []

    for symbol in symbols:

        url = "https://api.finnhub.io/api/v1/quote?"
        params = {
            # symbol: Котировка
            "symbol": symbol,
            "token": finnhub_key,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get("c")
            prices.append({"stock": symbol, "price": data})
    logging.info(f"Список сток: {prices}")
    return prices


def main_views_foo(
    data_time: str,
) -> dict:
    main_viewa_dict = {
        "greeting": get_greeting(),
        "cards": get_card_summary(df),
        "top_transactions": get_top_transactions(df),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices(finnhub_key),
    }
    json_data = json.dumps(main_viewa_dict, ensure_ascii=False, indent=4)
    return json_data


if __name__ == "__main__":
    data_time = "2024-04-06 19:40:15"
    # df = load_excel_to_dataframe(file_path)
    # print(get_greeting(data_time))
    # print(get_card_summary(df))
    # print(get_top_transactions(df))
    #
    # print(get_currency_rates())
    # print(get_stock_prices(api_key))

    print(main_views_foo(data_time))
