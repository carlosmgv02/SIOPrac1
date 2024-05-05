import pandas as pd

from db_manager import process_files
from config.warehouse_config import get_db_engine

directory = 'Dataset'
sql_query = 'SELECT * FROM titles limit 100'
session = get_db_engine()

if __name__ == '__main__':
    process_files('Dataset')





