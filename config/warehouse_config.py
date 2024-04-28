# config/warehouse_config.py
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.env_utils import get_env_value

POSTGRES_URI = get_env_value('DB_URI')

def get_db_session():
    engine = create_engine(POSTGRES_URI)
    Session = sessionmaker(bind=engine)
    return Session()

def get_db_engine():
    return create_engine(POSTGRES_URI)
