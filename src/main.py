import os

from src.reports import spending_by_category
from src.services import search_phone_numbers
from src.utils import load_excel_to_dataframe
from src.views import main_views_foo

current_dir = os.getcwd()
parrent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parrent_dir, "data")
file_path = os.path.join(data_dir, "operations.xls")
json_path = os.path.join(parrent_dir, "user_settings.json")

data_time = "2021-04-06 19:40:15"
category = "Фастфуд"


df = load_excel_to_dataframe(file_path)


def main(df, data_time, category):
    print(f"Функция главная \n\n\n\n\n\n {main_views_foo(data_time)}")
    print(f"Поиск по номеру телефона \n\n\n\n\n\n {search_phone_numbers(df)}")
    print(f"Траты за 3 месяца по выбранной категории \n\n\n\n\n\n {spending_by_category(df, category, data_time)}")


if __name__ == "__main__":
    main(df, data_time, category)
