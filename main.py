import pandas as pd

from db_manager import process_files
from logger.color_logger import setup_logger
import logging
from utils.scheduled_util import iniciar_tarea_en_hilo
from services import eda
from config.warehouse_config import get_db_engine

directory = 'Dataset'
sql_query = 'SELECT * FROM titles limit 100'
session = get_db_engine()

if __name__ == '__main__':
    process_files('Dataset')





