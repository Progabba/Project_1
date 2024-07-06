import os

from src.utils import load_excel_to_dataframe

current_dir = os.getcwd()
parrent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parrent_dir, 'data')
file_path = os.path.join(data_dir, 'operations.xls')
json_path = os.path.join(parrent_dir, 'user_settings.json')


load_excel_to_dataframe(file_path)
